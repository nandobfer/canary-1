#!usr/bin/bash

cmake --build build/linux-release
mv canary canary.bak
cp build/linux-release/bin/canary .