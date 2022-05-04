# Smile
<p align="center">
  <img width="150" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/it.mijorus.smile.png">
</p>

<p align="center">
  <img width="150" src="https://img.shields.io/endpoint?url=https://flathub-stats-backend.vercel.app/badges/it.mijorus.smile/shields.io.json">
</p>

Smile is a simple emoji picker for linux with **custom tags support**.


### Custom tags
... Wait what?

No matter how many tags we put, there is always going to be that one emoji you use every day which you expect to show up when you enter a specific query, but it doesn't. Smile wants to fix that, allowing the users to set their own custom tags for a specific emoji.

An example?  
Do you want 🌐 to show up when you search for "internet", but it is only tagged as "globe"? Select the icon using the arrow keys and press `Alt + T` to insert "internet" as custom tag.

<p align="center">
  <img width="500" src="https://raw.githubusercontent.com/mijorus/smile/master/docs/screenshot4.png">
</p>

### Custom shortcut
This app does not register its own system-wide shortcut, but you can create one simply by going in the system settings. Most, if not all, distrubutions let the user add shortcuts that trigger custom commands. 

You can create a shortcut for Smile by launching this command: `flatpak run it.mijorus.smile`

I believe that having all the shortcuts in once central panel is a much better user expecience than apps registering their own shortcuts separately.

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



## Download
<a href="https://flathub.org/apps/details/it.mijorus.smile" align="center">
  <img width="200" src="https://flathub.org/assets/badges/flathub-badge-i-en.png">
</a>

## Source
<a href="https://github.com/mijorus/smile" align="center">
  <img width="100" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png">
</a>

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



## Disclaimer
This is my first GTK app. If there is something wrong with the code, like say... it sucks, please let me know opening  a bug or a pull request
