#!/bin/bash
# Installs (or removes with 'remove') the facer-gpu-oc service: it applies the
# PredatorSense GPU overclock (core +100 MHz, memory +200 MHz on the PH315-55)
# while the platform profile is Turbo or Extreme, and removes it otherwise.
# Extra options for facer_gpu_oc.py can be given after the mode, e.g.:
#   sudo ./install_gpu_oc_service.sh install --core 100 --mem 200
mode=${1:-install}
shift
service=facer-gpu-oc
target=/usr/local/bin/facer_gpu_oc.py
unit=/etc/systemd/system/$service.service

if [[ $(id -u) -ne 0 ]]; then echo "Please run as root"; exit 1; fi

if systemctl list-unit-files "$service.service" >/dev/null 2>&1; then
	systemctl disable --now "$service" 2>/dev/null
fi
rm -f "$unit" "$target"

if [[ "$mode" == "install" ]]; then
	install -m 755 "$(dirname "$0")/facer_gpu_oc.py" "$target"
	cat << EOF > "$unit"
[Unit]
Description=Acer Predator GPU overclock in Turbo/Extreme (PredatorSense behaviour)
After=turbo-fan.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 -I $target $*
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
	systemctl daemon-reload
	systemctl enable --now "$service"
	systemctl --no-pager status "$service"
elif [[ "$mode" == "remove" ]]; then
	systemctl daemon-reload
	echo "$service removed"
else
	echo "Usage: $0 [install|remove] [facer_gpu_oc.py options]"
	exit 1
fi
