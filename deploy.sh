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

git show-ref refs/heads/master | awk -v date="$(date +"%Y-%m-%d %r")" '{ print $1, date }' > $DIR/version

tar -czf $DIR.tar $DIR

scp $DIR.tar seciot@$IP:deploy/
ssh seciot@$IP <REMOTESCRIPT>



rm $DIR.tar
rm $DIR/version
