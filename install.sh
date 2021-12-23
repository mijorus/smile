#! /usr/bin/bash
flatpak-builder --install --user --force-clean build/ it.mijorus.smile.json smile
flatpak run it.mijorus.smile
