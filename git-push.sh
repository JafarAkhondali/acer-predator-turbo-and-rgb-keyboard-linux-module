#!/bin/bash

#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

## ------------ COLORS ------------ ##

# Reset #
RESET_COLOR='\033[0m' # Text Reset

# Regular Colors #
Black='\033[0;30m'  Red='\033[0;31m'     Green='\033[0;32m'  Yellow='\033[0;33m'
Blue='\033[0;34m'   Purple='\033[0;35m'  Cyan='\033[0;36m'   White='\033[0;37m'

# Bold #
BBlack='\033[1;30m' BRed='\033[1;31m'    BGreen='\033[1;32m' BYellow='\033[1;33m'
BBlue='\033[1;34m'  BPurple='\033[1;35m' BCyan='\033[1;36m'  BWhite='\033[1;37m'

# Underline #
UBlack='\033[4;30m' URed='\033[4;31m'    UGreen='\033[4;32m' UYellow='\033[4;33m'
UBlue='\033[4;34m'  UPurple='\033[4;35m' UCyan='\033[4;36m'  UWhite='\033[4;37m'

# Background #
On_Black='\033[40m' On_Red='\033[41m'    On_Green='\033[42m' On_Yellow='\033[43m'
On_Blue='\033[44m'  On_Purple='\033[45m' On_Cyan='\033[46m'  On_White='\033[47m'

# High Intensity #
IBlack='\033[0;90m' IRed='\033[0;91m' IGreen='\033[0;92m' IYellow='\033[0;93m'      
IBlue='\033[0;94m' IPurple='\033[0;95m' ICyan='\033[0;96m' IWhite='\033[0;97m'      

# Bold High Intensity #
BIBlack='\033[1;90m' BIRed='\033[1;91m' BIGreen='\033[1;92m' BIYellow='\033[1;93m'
BIBlue='\033[1;94m' BIPurple='\033[1;95m' BICyan='\033[1;96m' BIWhite='\033[1;97m'

# High Intensity backgrounds #
On_IBlack='\033[0;100m' On_IRed='\033[0;101m' On_IGreen='\033[0;102m' On_IYellow='\033[0;103m'
On_IBlue='\033[0;104m' On_IPurple='\033[0;105m' On_ICyan='\033[0;106m' On_IWhite='\033[0;107m'

echo ""
echo -e "${BCyan}#############################${RESET_COLOR}"
echo -e "${BCyan}#      Git Push Script      #${RESET_COLOR}"
echo -e "${BCyan}#############################${RESET_COLOR}"

# get branch name (e.g master, main, etc... ) #
DEFAULT_BRANCH=$(git branch --show-current)
TARGET_BRANCH=${DEFAULT_BRANCH}

# get default commit message based on changes #
DEFAULT_COMMIT_MSG=""

# IFS -> Internal Field Separator
# IFS  in Bash. It is a special variable that determines how Bash recognizes word boundaries.
# By default, IFS is set to space, tab, and newline characters. 
while IFS=$'\n' read -r -d '' line;
    
    do

        status=$(echo "$line" | awk '{print $1}')
        file=$(echo "$line" | awk '{$1=""; print $0}' | sed -e 's/^[ \t]*//')

        case "$status" 
            
            in

                D)
                    # Deleted #
                    DEFAULT_COMMIT_MSG+="    ${BRed}==> deleted : $file${RESET_COLOR}"
                    DEFAULT_COMMIT_MSG+=""

                    ;;

                M)
                    # Modified #
                    DEFAULT_COMMIT_MSG+="    ${BCyan}==> modified : $file ${RESET_COLOR}"
                    DEFAULT_COMMIT_MSG+=""

                    ;;

                \?\?)

                    # Added #
                    DEFAULT_COMMIT_MSG+="    ${BGreen}==> added : $file ${RESET_COLOR}"
                    DEFAULT_COMMIT_MSG+=""

                    ;;

            esac
        
        # Add a newline character after each line #
        DEFAULT_COMMIT_MSG+="\n"

done < <(git status -s -z)

# Remove the trailing comma and space, if any #
DEFAULT_COMMIT_MSG=$(echo -e "$DEFAULT_COMMIT_MSG" | sed 's/, $//' | tr '\\' '\n')

# If no changes detected, use a default message #
if [ -z "$DEFAULT_COMMIT_MSG" ];
    
    then
        
        DEFAULT_COMMIT_MSG="   ==> NO changes"

fi

echo -e "\n${BRed}[*] Your Current Branch : ${BYellow}${DEFAULT_BRANCH}${RESET_COLOR}"

# get new updates if it founded #
echo -e "\n${BPurple}[+] Updating Repo... \n${RESET_COLOR}"
git pull 

echo -e "\n${BPurple}[+] The new changes in the repo:\n\n${BYellow}${DEFAULT_COMMIT_MSG}${RESET_COLOR}"

# Loop through all arguments #
while [[ $# -gt 0 ]];
    
    do
        
        case "$1" in

            -t|--target-branch)
                TARGET_BRANCH="$2"
                shift 2
                ;;

            -m|--commit-msg)
                DEFAULT_COMMIT_MSG="$2"
                shift 2
                ;;

            --create-pr)
                CREATE_PR=true
                TARGET_PR_BRANCH="$2"
                shift 2
                ;;
                
            *)
                # Ignore unrecognized options #
                shift
                ;;

        esac

done

echo -e "\n${BRed}[+] Target Branch : ${BYellow}${TARGET_BRANCH}${RESET_COLOR}"
if [ "${TARGET_BRANCH}" != "${DEFAULT_BRANCH}" ];
    
    then
        
        if git show-ref --verify --quiet "refs/heads/${TARGET_BRANCH}";
            
            then
                
                echo -e "${BBlue}  └──> Changing to the Target Branch: ${BYellow}${TARGET_BRANCH}${RESET_COLOR}"
                git checkout ${TARGET_BRANCH}

        else

            echo -e "${BBlue}  └──> Creating and changing to the Target Branch: ${BYellow}${TARGET_BRANCH}${RESET_COLOR}"
            git checkout -b ${TARGET_BRANCH}

        fi

fi


echo -e "\n${BPurple}[+] Adding new changes to the repo... \n${RESET_COLOR}"
git add --all .

# Check for a custom commit message #
if [ -n "${DEFAULT_COMMIT_MSG}" ];
    
    then
        
        echo ""
        git commit -m "${DEFAULT_COMMIT_MSG}"

fi

# push to Target Branch #
echo ""
git push -u origin ${TARGET_BRANCH}

# Check and create a pull request #
if [ "${CREATE_PR}" == true ] && [ -n "${TARGET_PR_BRANCH}" ];
    
    then
    
        echo -e "\n${BBlue}[+] Creating a pull request from ${BRed}${TARGET_BRANCH} ${BBlue}to ${BYellow}${TARGET_PR_BRANCH}...${RESET_COLOR}"
        gh pr create --base ${TARGET_PR_BRANCH} --head ${TARGET_BRANCH} --title "Pull Request: ${TARGET_BRANCH} to ${TARGET_PR_BRANCH}" --body "Please review and merge."

fi


# D O N E! #
echo -e "\n${BGreen}[✔] D O N E \n${RESET_COLOR}"
