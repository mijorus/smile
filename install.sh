#! /usr/bin/bash
flatpak-builder build/ it.mijorus.smile.json --user --install --force-clean
flatpak run it.mijorus.smile
