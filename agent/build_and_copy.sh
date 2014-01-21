#!/usr/bin/env bash


usage() {
  cat <<-USAGE
Usage: ${0##*/} [<option>...]
Build and copy client binary to <raspberry-ip>. 
Default:
  * go build
  * scp <ip>
  * ssh <ip>
Options:
  -u <ip or hostname> Raspberry Pi ip address or host name.   
USAGE
}


parse_options() {
  while getopts u:h: OPTNAME; do
    case $OPTNAME in
      u) HOST=$OPTARG;;
      h) usage; exit;;
      *) usage >&2; exit 1;;
    esac
  done
}


parse_options "$@"

if [ "x$HOST" == "x" ]; then
    usage >&2; exit 1;
    exit 1
fi

set -e
GOARCH=arm GOARM=5 GOOS=linux go build raspberry-workshop-ip-finder.go
scp raspberry-workshop-ip-finder pi@$HOST:~
ssh pi@$HOST
