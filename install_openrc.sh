#!/bin/bash
# This script can install or uninstall acer turbo fan service. It means, that your turbo fan button still will be available even after rebooting.
# To install service just run this script as the root (sudo) user.
# After installation you can manage it as a usual service manually. Example: 'systemctl start/stop turbo-fan',  'systemctl enable/disable turbo-fan'
# To uninstall service, run this script with 'remove' argument. Example: 'sudo bash ./install_service.sh remove'.
# Note!!! Before removing, don't forget to switch off the turbo button because you will have forever turbo fan :)
mode=${1:-install} # Allowed modes: "install" and "remove". Default: install.
service=turbo-fan # Service name
target_dir=/opt/turbo-fan # Instalation folder
service_dir=/etc/init.d/ # Service setup folder (where all services are stored)

echo "[Mode: $mode]";

# Sudo check
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

# Check systemctl is installed
if [[ -z "$(whereis rc-service | sed 's/systemctl: //')"  ]]; then echo "rc-service is not installed! If you aren't using openrc or aren't sure, use install_service.sh instead!"; exit 1; fi
# Check rsync is installed	
if [[ -z "$(whereis rsync | sed 's/rsync: //')"  ]]; then echo "rsync is not installed"; exit 1; fi

if [[ "$mode" == "install" || "$mode" == "remove" ]]; then
	# Check service is presented and remove if yes.
	if [[ "$(rc-update | grep $service)" ]]; then
		echo "['$service' service is presented. Remove it.]";
		rc-service $service stop;
		rc-service del $service default;
		rm $service_dir/turbo-fan
	fi
		
	# Remove old files
	echo "[Remove old data]";
	rm -rvf $target_dir;
fi;

if [[ "$mode" == "install" ]]
then
	echo "[Create directories]";
	mkdir -p $target_dir

	echo "[Copy new data]";
	rsync -av ./* $target_dir --exclude=".git/*"

	echo "[Create turbo-fan service]"
	cat << EOF > $service_dir/turbo-fan
#!/sbin/openrc-run
depend() {
	after bootmisc consolefont modules netmount
	after quota keymaps
	after elogind
	use dbus xfs
}

start() {
	local EXE NAME PIDFILE AUTOCLEAN_CGROUP
 	/sbin/rmmod acer_wmi
	/sbin/modprobe wmi
	/sbin/modprobe sparse-keymap
	/sbin/modprobe video
	/sbin/insmod $target_dir/src/facer.ko
	# You can also just make it launch $target_dir/install.sh by uncommenting the line below and removing everything starting from /sbin/rmmod acer_wmi to /sbin/insmod
	# /bin/bash $target_dir/src/facer.ko
}

stop() {
	/sbin/rmmod facer
}

# vim: set ts=4 :
EOF
	chmod +x $service_dir/turbo-fan
	rc-update add $service default
	rc-service $service start
fi
