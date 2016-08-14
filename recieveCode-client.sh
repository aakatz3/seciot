#!/bin/bash -e
cd deploy
tar -xzf client.tgz
cd client
cp version ../../
rm -rfv /var/www/seciothome/
mv * /var/www/
rm -rfv /home/seciot/deploy/
mkdir /home/seciot/deploy
