#!/usr/bin/env python3
"""
GPU overclock that follows the Acer platform profile, like PredatorSense.

On Windows, switching an operating mode model (e.g. Predator PH315-55) to
Extreme or Turbo makes the PredatorSense service apply a P0 clock offset to the
NVIDIA GPU through NvAPI_GPU_SetPstates20, read from its PredatorSense.ini:

    [PCI\\VEN_10DE&DEV_24E0&SUBSYS_15991025]
    Quiet=0  Default=0  Extreme=100  Turbo=100                  (core, MHz)
    RAM_Quiet=0  RAM_Default=0  RAM_Extreme=200  RAM_Turbo=200  (memory, MHz)

The BIOS does nothing with the OC level PredatorSense also sends over WMI, so
the overclock has to be applied from userspace. This daemon does it with NVML,
the Linux counterpart of NvAPI, whenever /sys/firmware/acpi/platform_profile
changes (turbo key, mode key, power-profiles-daemon, or a write to the file).

As PredatorSense does, the overclock is only applied on AC power with at least
40% battery, and removed when the battery drops below 30%.

Memory offsets: NvAPI counts them on the memory clock that nvidia-smi reports
(7001 MHz on an RTX 3070 Ti Laptop), NVML counts them in transfer rate, twice
that. An NVML offset of +200 moves the reported clock from 7000 to 7100 MHz, so
the +200 MHz of PredatorSense is an NVML offset of +400.

Needs root (NVML refuses clock offsets otherwise). Only the Python standard
library and libnvidia-ml.so.1 (shipped with the NVIDIA driver) are used.
"""

import argparse
import ctypes
import glob
import os
import select
import signal
import sys
import time

PROFILE_PATH = "/sys/firmware/acpi/platform_profile"

NVML_SUCCESS = 0
NVML_CLOCK_GRAPHICS = 0
NVML_CLOCK_MEM = 2
NVML_PSTATE_0 = 0

# PredatorSense battery thresholds for overclocking
BATTERY_RESUME = 40
BATTERY_STOP = 30


class NvmlClockOffset(ctypes.Structure):
    _fields_ = [
        ("version", ctypes.c_uint),
        ("type", ctypes.c_int),
        ("pstate", ctypes.c_int),
        ("clockOffsetMHz", ctypes.c_int),
        ("minClockOffsetMHz", ctypes.c_int),
        ("maxClockOffsetMHz", ctypes.c_int),
    ]


NVML_CLOCK_OFFSET_V1 = ctypes.sizeof(NvmlClockOffset) | (1 << 24)


def log(msg):
    print(msg, flush=True)


class Nvml:
    """Short-lived NVML session: holding NVML open would keep the GPU awake."""

    def __init__(self, index):
        self.lib = ctypes.CDLL("libnvidia-ml.so.1")
        self._check(self.lib.nvmlInit_v2(), "nvmlInit")
        self.handle = ctypes.c_void_p()
        try:
            self._check(self.lib.nvmlDeviceGetHandleByIndex_v2(
                index, ctypes.byref(self.handle)), "nvmlDeviceGetHandleByIndex")
        except Exception:
            self.lib.nvmlShutdown()
            raise

    def _check(self, ret, what):
        if ret != NVML_SUCCESS:
            self.lib.nvmlErrorString.restype = ctypes.c_char_p
            raise RuntimeError(f"{what}: {self.lib.nvmlErrorString(ret).decode()}")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.lib.nvmlShutdown()

    def offsets(self):
        core, mem = ctypes.c_int(), ctypes.c_int()
        self._check(self.lib.nvmlDeviceGetGpcClkVfOffset(
            self.handle, ctypes.byref(core)), "nvmlDeviceGetGpcClkVfOffset")
        self._check(self.lib.nvmlDeviceGetMemClkVfOffset(
            self.handle, ctypes.byref(mem)), "nvmlDeviceGetMemClkVfOffset")
        return core.value, mem.value

    def set_offsets(self, core, mem):
        if hasattr(self.lib, "nvmlDeviceSetClockOffsets"):
            # Driver 555+: P0 offsets, like NvAPI_GPU_SetPstates20 on Windows
            for clock, value in ((NVML_CLOCK_GRAPHICS, core), (NVML_CLOCK_MEM, mem)):
                info = NvmlClockOffset(version=NVML_CLOCK_OFFSET_V1, type=clock,
                                       pstate=NVML_PSTATE_0, clockOffsetMHz=value)
                self._check(self.lib.nvmlDeviceSetClockOffsets(
                    self.handle, ctypes.byref(info)), "nvmlDeviceSetClockOffsets")
            return
        # Older drivers: the same offsets through the VF curve API
        self._check(self.lib.nvmlDeviceSetGpcClkVfOffset(self.handle, core),
                    "nvmlDeviceSetGpcClkVfOffset")
        self._check(self.lib.nvmlDeviceSetMemClkVfOffset(self.handle, mem),
                    "nvmlDeviceSetMemClkVfOffset")


def read(path, default=None):
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return default


def power_supplies():
    """Return (on_ac, battery_percent or None)."""
    on_ac, capacity = False, None
    for supply in glob.glob("/sys/class/power_supply/*"):
        kind = read(os.path.join(supply, "type"))
        if kind == "Mains" and read(os.path.join(supply, "online")) == "1":
            on_ac = True
        elif kind == "Battery" and read(os.path.join(supply, "scope"), "System") == "System":
            value = read(os.path.join(supply, "capacity"))
            if value is not None and value.isdigit():
                capacity = int(value)
    return on_ac, capacity


def gpu_awake():
    """False when the dGPU is runtime-suspended: NVML would wake it up."""
    for dev in glob.glob("/sys/bus/pci/drivers/nvidia/0000:*"):
        if read(os.path.join(dev, "power/runtime_status"), "active") != "active":
            return False
    return True


class Daemon:
    def __init__(self, args):
        self.args = args
        self.oc_profiles = set(args.profiles.split(","))
        self.battery_ok = True
        self.applied = None  # (core, mem) in NVML units, as last read back

    def wanted(self):
        profile = read(PROFILE_PATH, "")
        on_ac, capacity = power_supplies()
        if capacity is not None:
            if capacity < BATTERY_STOP:
                self.battery_ok = False
            elif capacity >= BATTERY_RESUME:
                self.battery_ok = True
        if profile in self.oc_profiles and on_ac and self.battery_ok:
            return profile, (self.args.core, self.args.mem * 2)
        return profile, (0, 0)

    def sync(self):
        profile, target = self.wanted()
        # Nothing applied and nothing wanted: leave the GPU alone (and asleep)
        if target == (0, 0) and self.applied == (0, 0):
            return
        # While overclocked, offsets are read back on every tick so they get
        # applied again if a GPU reset or a resume from suspend dropped them.
        if not gpu_awake():
            return
        try:
            with Nvml(self.args.gpu) as nvml:
                current = nvml.offsets()
                if current != target:
                    nvml.set_offsets(*target)
                    current = nvml.offsets()
                    log(f"profile={profile}: GPU offsets core {current[0]:+d} MHz, "
                        f"memory {current[1]:+d} (NVML) / {current[1] // 2:+d} MHz (NvAPI)")
                self.applied = current
        except (OSError, RuntimeError) as err:
            self.applied = None
            log(f"NVML: {err}")

    def run(self):
        fd = os.open(PROFILE_PATH, os.O_RDONLY)
        poller = select.poll()
        poller.register(fd, select.POLLPRI | select.POLLERR)
        while True:
            self.sync()
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                os.read(fd, 64)  # sysfs needs a read before the next poll
            except OSError:
                # facer was unloaded: let systemd restart us once it is back
                self.reset()
                sys.exit(f"facer_gpu_oc: {PROFILE_PATH} went away")
            poller.poll(self.args.interval * 1000)

    def reset(self):
        if self.applied not in (None, (0, 0)):
            try:
                with Nvml(self.args.gpu) as nvml:
                    nvml.set_offsets(0, 0)
                log("GPU offsets reset to 0")
            except (OSError, RuntimeError) as err:
                log(f"NVML: {err}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--core", type=int, default=100,
                        help="core offset in MHz (PredatorSense: Turbo=100)")
    parser.add_argument("--mem", type=int, default=200,
                        help="memory offset in MHz, NvAPI/PredatorSense units "
                             "(RAM_Turbo=200); NVML gets twice this value")
    parser.add_argument("--profiles", default="performance,balanced-performance",
                        help="platform profiles that get the overclock "
                             "(performance = Turbo, balanced-performance = Extreme)")
    parser.add_argument("--gpu", type=int, default=0, help="NVML GPU index")
    parser.add_argument("--interval", type=int, default=5,
                        help="seconds between checks of power source and offsets")
    args = parser.parse_args()

    if os.geteuid() != 0:
        sys.exit("facer_gpu_oc: must run as root (NVML clock offsets)")
    if not os.path.exists(PROFILE_PATH):
        sys.exit(f"facer_gpu_oc: {PROFILE_PATH} missing, is facer loaded?")

    daemon = Daemon(args)

    def stop(*_):
        daemon.reset()
        sys.exit(0)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    daemon.run()


if __name__ == "__main__":
    main()
