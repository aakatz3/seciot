#!/bin/bash -e

DIR=$1
IP=$2

function die() {
    echo >&2 $*
    exit 1
}


if [[ $IP == "" ]]; then
    die "Usage: $0 DIR IP"
fi


case $DIR in
    server)
	;;
    client)
	;;
    *)
	die "First arg must be client or server"
	;;
esac

if [[ $(git status --porcelain 2>/dev/null| egrep "^(M| M)" | wc -l) != "0" ]]; then
   die "There are uncommited/untracked files. Please commit and push."
fi



git show-ref refs/heads/master | awk -v date="$(date +"%Y-%m-%d %r")" '{ print $1, date }' > $DIR/version

tar -czf $DIR.tar $DIR

scp $DIR.tar seciot@$IP:deploy/
ssh seciot@$IP <REMOTESCRIPT>

##TODO
#Make sure repo is commited (git status), say uncommited and die FIRST
#tag the repo, and write to file
#write remote script



rm $DIR.tar
rm $DIR/version
