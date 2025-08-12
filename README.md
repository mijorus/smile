# Smile
<p align="center">
  <img width="150" src="docs/it.mijorus.smile.svg">
</p>


<p align="center">
 <a href="https://flatstat.mijorus.it/app/it.mijorus.smile"  align="center">
  <img width="150" src="https://img.shields.io/endpoint?url=https://flathub-stats-backend.vercel.app/badges/it.mijorus.smile/shields.io.json">
</a>
</p>


##  Support me

<a href="https://ko-fi.com/mijorus" align="center">
  <img width="250" src="https://mijorus.it/kofi-support.png">
</a>

##  1. Download

### Get from Flathub
<a href="https://flathub.org/apps/details/it.mijorus.smile" align="center">
  <img width="200" src="https://flathub.org/assets/badges/flathub-badge-i-en.png">
</a>

### Automatically paste with the GNOME Extension

**Requires Smile 2.4.0+**

<a href="https://extensions.gnome.org/extension/6096/smile-complementary-extension" align="center">
  <img width="200" src="docs/gnome-extension.svg">
</a>

###  1.1 Source
<a href="https://github.com/mijorus/smile" align="center">
  <img width="100" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png">
</a>

Note: Flathub and Github are the only official release channels for Smile. Any release on external marketplaces or packaging formats are unofficial and not supported by me.

### 1.2 Center new windows on GNOME

Use the following command to make Smile and any new window be centered:
```
gsettings set org.gnome.mutter center-new-windows true
```

##  2. Features

Smile is a simple emoji picker for linux with **custom tags support**.

###  2.1. Localized tags + english fallback!

#### English fallback!
Go to `Preferences > Localized tags > Merge localized tags`!

###  2.2. Custom tags
No matter how many tags we put in, there is always going to be that one emoji which you expect to show up when you search, but it doesn't.

An example?  
Do you want 🌐 to show up when you search for "internet", but it is only tagged as "globe"? 

Select the icon using the arrow keys and press `Alt + T` or `Middle Click` to open the custom tag manager.

<p align="center">
  <img width="500" src="docs/screenshot4.png">
</p>

###  2.3. Custom shortcut
This app does not register its own system-wide shortcut, but you can create your custom shortcut for Smile by launching this command: 

`flatpak run it.mijorus.smile`

###  2.4. Skintone selector

Press `Alt + E` or `Right Click` on any emoji with the **rounded top-right** corner (see screenshot below).
<p align="center">
  <img width="500" src="docs/screenshot10.png">
</p>

###  2.5. Multi selection
Use `Shift + Enter` to select multiple emojis; use `Ctrl+Enter` to quit without selecting an additional emoji
<p align="center">
  <img width="500" src="docs/screenshot11.png">
</p>


##  3. Changelog
Please check out [https://smile.mijorus.it/changelog](https://smile.mijorus.it/changelog)

##  5. Third party licences
Awesome resources that made Smile possible:

- [Openmoji](https://openmoji.org/) for the emoji list and english tags
- [Emojibase](https://github.com/milesj/emojibase) for the translated tags available since version 1.70

##  6. Building 
You will need:
- flatpak
- flatpak-builder
- org.gnome.Platform 48
- org.gnome.Sdk 48
- pango devel kit

```sh
# Fedora
sudo dnf install pango-devel

# Ubuntu
sudo apt-get install libsdl-pango-dev 

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

##  7. Thanks to

- [Emote](https://github.com/tom-james-watson/Emote) for the inspiration and some code

##  8. Some more screenshots
<p align="center">
  <img width="500" src="docs/screenshot1.png">
</p>
