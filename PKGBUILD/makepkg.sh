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
BUILDPKG () {

    echo -e "\nRemoving olda PKGs \n"
    rm ./*.pkg.tar.zst
	echo -e "\nBuilding Package...... \n"
	makepkg -s -f
	
    rm -rf acer-predator-turbo-and-rgb-keyboard-linux-module src pkg
}

# Execute
BUILDPKG