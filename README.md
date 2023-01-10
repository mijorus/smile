# Smile
<p align="center">
  <img width="150" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/it.mijorus.smile.png">
</p>


<p align="center">
 <a href="https://flatstat.mijorus.it/app/it.mijorus.smile"  align="center">
  <img width="150" src="https://img.shields.io/endpoint?url=https://flathub-stats-backend.vercel.app/badges/it.mijorus.smile/shields.io.json">
</a>
</p>

## Download
<a href="https://flathub.org/apps/details/it.mijorus.smile" align="center">
  <img width="200" src="https://flathub.org/assets/badges/flathub-badge-i-en.png">
</a>

Note: Flathub and Github are the only official release channels for Smile. Any release on external marketplaces or packaging formats are unofficial and not supported by me.

## Features

Smile is a simple emoji picker for linux with **custom tags support**.

### Localized tags!
Go to `Preferences > Localized tags`

#### English fallback!
Go to `Preferences > Localized tags > Merge localized tags`!

### Custom tags
Select the icon using the arrow keys and press `Alt + T` to insert one or more custom tags.

<p align="center">
  <img width="500" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/screenshot4.png">
</p>

### Custom shortcut

Please open your system settings and create a global shortcut for this command: `flatpak run it.mijorus.smile`

### Skintone selector

Press `Alt + E` or `Right Click` on any emoji with the **rounded top-right** corner (see screenshot below).
<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/39067225/166464525-fb2a56ef-581d-4c08-ad23-4bcd245e7fdd.png">
</p>

### Multi selection
Use `Shift + Enter` to select multiple emojis; use `Ctrl+Enter` to quit without selecting an additional emoji
<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/39067225/166487730-e1b6b686-5095-4ddb-8ba9-723b3d53101d.png">
</p>


## Changelog
Please check out [https://smile.mijorus.it/changelog](https://smile.mijorus.it/changelog)

## Source
<a href="https://github.com/mijorus/smile" align="center">
  <img width="100" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png">
</a>

## Third party licences
Awesome resources that made Smile possible:

- [Openmoji](https://openmoji.org/) for the emoji list and english tags
- [Emojibase](https://github.com/milesj/emojibase) for the translated tags available since version 1.70

## Building 
You will need:
- flatpak
- flatpak-builder
- flatpak-builder
- org.gnome.Platform 41
- org.gnome.Sdk 41

```sh
git clone https://github.com/mijorus/smile.git
cd smile

# kill any instance of Smile
flatpak kill it.mijorus.smile

# to run the app:
flatpak-builder build/ it.mijorus.smile.json --user --force-clean
flatpak-builder --run build/ it.mijorus.smile.json smile

# to install the app
flatpak-builder build/ it.mijorus.smile.json --user --install --force-clean
```

## Thanks to

- [Emote](https://github.com/tom-james-watson/Emote) for the inspiration and some code

## Some more screenshots
<p align="center">
  <img width="500" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/screenshot1.png">
</p>
<p align="center">
  <img width="500" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/screenshot2.png">
</p>
<p align="center">
  <img width="500" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/screenshot3.png">
</p>
<p align="center">
  <img width="500" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/screenshot5.png">
</p>

