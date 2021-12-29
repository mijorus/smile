#! /usr/bin/bash
flatpak kill it.mijorus.smile
flatpak-builder build/ it.mijorus.smile.json --user --force-clean
flatpak-builder --run build/ it.mijorus.smile.json smile