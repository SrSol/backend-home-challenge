#!/bin/bash

tar --exclude ".git/" -cvf app.tar ../
docker build -t $1 .
rm -f app.tar
