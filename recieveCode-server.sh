#!/bin/bash -e
cd deploy
tar -xzf server.tgz
cd server
cp version ../../
rm -rfv /var/www/seciotcloud/
mv * /var/www/
rm -rfv /home/seciot/deploy/
mkdir /home/seciot/deploy
