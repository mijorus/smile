#! /usr/bin/bash
flatpak-builder build/ it.mijorus.smile.json --user --ccache --force-clean && flatpak-builder --run build/ it.mijorus.smile.json smile