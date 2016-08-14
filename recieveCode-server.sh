#!/bin/bash -e
cd deploy
tar -xzf server.tgz
cd server
cp version ../
mv * /var/www/
cd ..
rm -rfv server/
rm server.tgz
