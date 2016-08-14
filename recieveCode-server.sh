#!/bin/bash -e
cd deploy
tar -xzf server.tgz
cd server
mv * /var/www/
