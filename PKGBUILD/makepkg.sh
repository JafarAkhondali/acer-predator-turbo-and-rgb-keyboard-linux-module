#
# Copyright (C) 2022 Mahmoud Mohamed (Ozil)  <https://github.com/mmsaeed509>
# LICENSE © GNU-GPL3
#


# Script Termination
exit_on_signal_SIGINT () {
    { printf "\n\n%s\n" "Script interrupted." 2>&1; echo; }
    exit 0
}

exit_on_signal_SIGTERM () {
    { printf "\n\n%s\n" "Script terminated." 2>&1; echo; }
    exit 0
}

trap exit_on_signal_SIGINT SIGINT
trap exit_on_signal_SIGTERM SIGTERM

# Build packages (create a binary package -> pkg.pkg.tar.zst)
build_pkg () {
	echo -e "\nBuilding Package...... \n"
	makepkg -s 
	
}

# Execute
build_pkg