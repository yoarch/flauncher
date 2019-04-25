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
</pre>

# configuration
the settings defining the command to be run for any extension type are located in the *~/.config/flauncher/launchers.json* json file.

if this file doesn't exist, copy the default one located in *~/.config/flauncher/launchers.json* and configure it as you wish.

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
  "libreoffice_writer": {
    "type": "lonely",
    "exts": ["odt"],
    "cmd": "libreoffice --writer"
  },
  "libreoffice_calc": {
    "type": "lonely",
    "exts": ["ods"],
    "cmd": "libreoffice --calc"
  },
  "pdf": {
    "type": "lonely",
    "exts": ["pdf"],
    "cmd": "evince -f"
  },
  "rar": {
    "type": "archive_a",
    "exts": ["rar"],
    "cmd": "unrar x"
  },
  "tar": {
    "type": "archive_a",
    "exts": ["tar"],
    "cmd": "tar -xvf"
  },
  "tar_gz": {
    "type": "archive_a",
    "exts": ["tar.gz"],
    "cmd": "tar -zxvf"
  },
  "tar_xz": {
    "type": "archive_b",
    "exts": ["tar.xz"],
    "cmd": "tar --directory FOLDER_PATH -xJf ARCHIVE_PATH"
  },
  "tar_bz2": {
    "type": "archive_a",
    "exts": ["tar.bz2"],
    "cmd": "tar jxvf"
  },
  "text": {
    "type": "lonely",
    "exts": ["text", "txt", "conf", "sh", "py", "note", "log", "c", "h", "js", "tmp", "json", "csv", "java", "xml", "tex", "js"],
    "cmd": "atom"
  },
  "tgz": {
    "type": "archive_a",
    "exts": ["tgz"],
    "cmd": "tar -xvzf"
  },
  "video": {
    "type": "playlist",
    "exts": ["avi", "mpeg", "mp4", "ogg", "quicktime", "webm", "mp2t", "flv", "mov", "webm", "mkv", "mts", "vob", "ogv", "drc", "gif", "gifv", "mng", "mts", "m2ts", "mwv", "yuv", "rm", "rmvb", "asf", "amv", "m4v", "mpg", "mpe", "mpv", "m2v", "svi", "3gp", "3g2", "mxf", "roq", "nsv", "f4v", "f4p", "f4a", "f4b"],
    "cmd": "mpv -fs --loop-playlist -script-opts=osc-hidetimeout=2000"
  },
  "zip": {
    "type": "archive_b",
    "exts": ["zip"],
    "cmd": "unzip -d FOLDER_PATH ARCHIVE_PATH"
  }
}
```

by default any audio and video files are launched with **mpv**, any image with **feh**, any pdf with **evince** and any text with the **atom** editor.
But feel free to customize it with your application launcher preferences.

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

# suggestions
use the **o** command to open any file:<br/>
```sh
alias o='flauncher'
```
