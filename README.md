# flauncher
universal file launcher for terminal

Launch any file in terminal with one unique command. flauncher works as a command router and launches the entered files with the according application regarding your preferences settings.

flauncher deals with **audio, image, libreoffice-writer (odt), libreoffice-calc (ods), pdf, rar, tar, tar.gz, tar.xz, tar.bz2, text, tgz, zip and video** files.

# installation
```sh
with pip:
sudo pip3 install flauncher

with yay:
yay -a flauncher

with yaourt:
yaourt -a flauncher
```

# compatibility
python >= 3


# usage
<pre>
<b>flauncher</b> [<b>FILE_PATH_01 FILE_PATH_02 ...</b>]
<b>options:</b>
<!-- -->         <b>-h, --help</b>        show this help message and exit
<!-- -->         <b>-m [mode]</b>         select another mode than the default launch one to open another conf file than launch.json
</pre>

# configuration
The settings defining the command to be run for any extension type are located in the *~/.config/flauncher/launch.json* json file.

If this file doesn't exist, copy the default one located in *~/.config/flauncher/launch.json* and configure it as you wish.

```sh
{
  "audio": {
    "type": "playlist",
    "exts": ["mp3", "wav", "m4a", "aac", "mp1", "mp2", "flac", "aa", "aax", "act", "aiff", "amr", "ape", "au", "awb", "dct", "dss", "dvf", "gsm", "iklax", "ivs", "m4b", "m4p", "mmf", "mpc", "msv", "nmf", "nsf", "oga", "mogg", "opus", "ra", "raw", "sin", "tta", "vox", "wma", "wv", "8svx"],
    "cmd": "mpv -fs --loop-playlist -script-opts=osc-hidetimeout=6000 --player-operation-mode=pseudo-gui"
  },
  "image": {
    "type": "playlist",
    "exts": ["jpg", "jpeg", "png", "tif", "gif", "bmp", "pjpeg", "jfif", "exif", "tiff", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat", "bpg"],
    "cmd": "feh -d -Y -F"
  },
  ...
  ...
}
```

By default any audio and video files are launched with **mpv**, any image with **feh**, any pdf with **evince**, any text with the **atom** editor, etc.
But feel free to customize it with your application preferences.

# examples
for **help**:<br/>
```sh
flauncher -h
or
flauncher --help
```

launch a **pdf**, a **zip**, a **tar.gz** and a **mp3**:<br/>
```sh
flauncher titi.pdf toto/tutu.zip toto/tutu.tar.gz toto/tata/tutu.mp3
```


# custom mode
Define others modes corresponding to others conf files with the **-m** parameter.
When specifying the **-m** parameter, you have to precise the **mode** name just after it corresponding to the *~/.config/flauncher/**mode**.json* conf file.
**-m edit** will use the *~/.config/flauncher/edit.json* conf file rather than the default launch.json one.


# suggestions
Use the **o** command to launch any file:<br/>
```sh
alias o='flauncher'
```

And the **e** command to edit any file:<br/>
```sh
alias e='flauncher -m edit'
```
