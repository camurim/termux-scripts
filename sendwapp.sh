#!/data/data/com.termux/files/usr/bin/env bash

USER=${USER:-$(whoami)}
HOME=${HOME:-/home/$USER}
SCRIPTNAME=$(basename $0)

# Cores
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
BOLDRED='\033[1;31m'
NC='\033[0m'

if [ $# -lt 2 ]; then
    printf "${RED}SINTAXE: $SCRIPTNAME <USER> <MESSAGE>${NC}\n" >&2
    exit 1
fi

if [ ! -f "$HOME/.wappapikey" ]; then
    printf "${RED}The configuration file does not exists in your home directory!${NC}\n" >&2
    exit 1
fi

urlencode() {
  local LC_ALL=C
  local string="$*"
  local length="${#string}"
  local char

  for (( i = 0; i < length; i++ )); do
    char="${string:i:1}"
    if [[ "$char" == [a-zA-Z0-9.~_-] ]]; then
      printf "$char"
    else
      printf '%%%02X' "'$char"
    fi
  done
  printf '\n' # opcional
}

phone=$(cat "$HOME/.wappapikey" | awk -F '|' -v "wpuser=$1" '$1 == wpuser {print $2}')
apikey=$(cat "$HOME/.wappapikey" | awk -F '|' -v "wpuser=$1" '$1 == wpuser {print $3}')
text=$(urlencode $2)

if [ ! -z $phone ] && [ ! -z $apikey ] && [ ! -z $text ]; then
    resultAux=$(curl -s "https://api.callmebot.com/whatsapp.php?phone=$phone&apikey=$apikey&text=$text")
    result=$(echo $resultAux | sed -e 's/<[^>]*>/\\n/g')

    printf "${BLUE}${result}${NC}\n" >&2
    exit 0
else
    printf "${RED}ERROR: Error reading properties!${NC}"
    exit 1
fi
