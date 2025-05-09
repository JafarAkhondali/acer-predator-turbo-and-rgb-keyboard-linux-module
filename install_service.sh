#!/bin/bash
# This script can install or uninstall acer turbo fan service. It means, that your turbo fan button still will be available even after rebooting.
# To install service just run this script as the root (sudo) user.
# After installation you can manage it as a usual service manually. Example: 'systemctl start/stop turbo-fan',  'systemctl enable/disable turbo-fan'
# To uninstall service, run this script with 'remove' argument. Example: 'sudo bash ./install_service.sh remove'.
# Note!!! Before removing, don't forget to switch off the turbo button because you will have forever turbo fan :)
mode=${1:-install} # Allowed modes: "install" and "remove". Default: install.
service=turbo-fan # Service name
target_dir=/opt/turbo-fan # Instalation folder
service_dir=/etc/systemd/system # Service setup folder (where all services are stored)
service_start_delay=5 # Delay in seconds before the service starts.

echo "[Mode: $mode]";

# Sudo check
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

# Check systemctl is installed
if [[ -z "$(whereis systemctl | sed 's/systemctl: //')"  ]]; then echo "systemctl is not installed"; exit 1; fi
# Check rsync is installed	
if [[ -z "$(whereis rsync | sed 's/rsync: //')"  ]]; then echo "rsync is not installed"; exit 1; fi

if [[ "$mode" == "install" || "$mode" == "remove" ]]; then
	# Check service is presented and remove if yes.
	if [[ "$(systemctl --type=service | grep $service)" ]]; then
		echo "['$service' service is presented. Remove it.]";
		systemctl stop $service;
		systemctl disable $service;
		rm $service_dir/turbo-fan.service
		systemctl daemon-reload
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
	cat << EOF > $service_dir/turbo-fan.service
[Unit]
Description = Enables turbo button
After=sysinit.target
StartLimitIntervalSec=$service_start_delay

[Service]
Type=simple
Restart=no
RemainAfterExit=yes
User=root
WorkingDirectory=$target_dir
ExecStart=/bin/bash $target_dir/service.sh
ExecStop=/bin/bash ./uninstall.sh

[Install]
WantedBy=multi-user.target
EOF
	chown -R root:root $target_dir

KERNELVERSION=$(uname -r)

    cat << EOF > $target_dir/service.sh
KERNELVERSION="$KERNELVERSION"
cd $target_dir

rm /dev/acer-gkbbl-0 /dev/acer-gkbbl-static-0 -f

if [ "\$(uname -r)" != "\$KERNELVERSION" ] || [ ! -f $target_dir/src/facer.ko ]; then
	make clean
    source ./install.sh
	sed -i "s/^KERNELVERSION.*/KERNELVERSION=\"\$(uname -r)\"/" $target_dir/service.sh
else
	rmmod acer_wmi
	rmmod facer
	modprobe wmi
	modprobe sparse-keymap
	modprobe video
	insmod $target_dir/src/facer.ko
fi
EOF

	#locking down service file for security
	chown -R root:root $target_dir
	chmod 744 $target_dir/service.sh

	systemctl daemon-reload
	systemctl start $service
	systemctl enable $service
fi
