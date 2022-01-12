#! /usr/bin/bash
python3 ./emoji_list/generate_emoji_dict.py
flatpak kill it.mijorus.smile
flatpak-builder build/ it.mijorus.smile.json --user --install --force-clean
