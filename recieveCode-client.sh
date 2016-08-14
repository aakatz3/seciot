#!/bin/bash -e
cd deploy
tar -xzf client.tgz
cd client
mv * /var/www/
