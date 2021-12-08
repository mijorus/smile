#! /usr/bin/bash
flatpak-builder build/ it.mijorus.simba.json --user --ccache --force-clean && flatpak-builder --run build/ it.mijorus.simba.json simba