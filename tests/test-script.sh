#! /usr/bin/bash

flatpak-builder build/ it.mijorus.smile.json --user --force-clean

flatpak-builder --run build/ it.mijorus.smile.json smile &
sleep 2

flatpak kill it.mijorus.smile

appstream-util validate data/it.mijorus.smile.appdata.xml.in