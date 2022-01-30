#! /usr/bin/bash
flatpak kill it.mijorus.smile
flatpak-builder build/ it.mijorus.smile.json --user --install --force-clean
