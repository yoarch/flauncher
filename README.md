# Flauncher
Universal CLI file launcher

Launch any file in terminal with one unique command. flauncher works as a command router and launches the input files with the according application/program regarding your settings preferences. Can also be imported in your own python codes.

Then, flauncher can deal with any file type such as **audio, image, libreoffice-writer (odt), libreoffice-calc (ods), pdf, rar, tar, tar.gz, tar.xz, tar.bz2, text, tgz, zip, video, etc.** files.

# Installation
```sh
With pip:
sudo pip3 install flauncher

With yay:
yay -a flauncher

With yaourt:
yaourt -a flauncher
```

# Compatibility
python >= 3


# Usage
<pre>
<b>flauncher</b> [<b>FILE_PATH_01 FILE_PATH_02 ...</b>]
<b>options:</b>
<!-- -->         <b>-h, --help</b>        show this help message and exit
<!-- -->         <b>-m [mode]</b>         select another mode than the default open one to open another conf file than open.json
</pre>

# Configuration
The settings defining the command to be run for any extension type are located in the *~/.config/flauncher/open.json* json file.

If this file doesn't exist, copy the default one located in *usr/lib/flauncher/open.json* and configure it as you wish.

```sh
{
        "files":
        {
                "audio": {
                  "mode": "playlist",
                  "exts": ["mp3", "wav", "m4a", "aac", "mp1", "mp2", "flac", "aa", "aax", "act", "aiff", "amr", "ape", "au", "awb", "dct", "dss", "dvf", "gsm", "iklax", "ivs", "m4b", "m4p", "mmf", "mpc", "msv", "nmf", "nsf", "oga", "mogg", "opus", "ra", "raw", "sin", "tta", "vox", "wma", "wv", "8svx"],
                  "app": "mpv",
                  "args": "--fs-screen=all -fs --loop-playplaylist --script-opts=osc-hidetimeout=6000 --player-operation-mode=pseudo-gui"
                },
                "graphical": {
                  "mode": "individual",
                  "exts": ["xcf"],
                  "app": "gimp",
                  "args": null
                },
                "image_bitmap": {
                  "mode": "playlist",
                  "exts": ["jpg", "jpeg", "png", "tif", "gif", "bmp", "pjpeg", "jfif", "exif", "tiff", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat", "bpg"],
                  "app": "sxiv",
                  "args": "-bf"
                },
                "libreoffice_writer": {
                  "mode": "individual",
                  "exts": ["odt", "doc", "docx", "docs"],
                  "app": "libreoffice --writer",
                  "args": null
                },
                "markup": {
                  "mode": "individual",
                  "exts": ["ad", "md", "adoc"],
                  "app": "brave",
                  "args": "-a"
                },
                "python": {
                  "mode": "individual",
                  "exts": ["py"],
                  "app": "pycharm",
                  "args": null
                },
                "pdf": {
                  "mode": "individual",
                  "exts": ["pdf"],
                  "app": "brave",
                  "args": "-a"
                },
                "rar": {
                  "mode": "archive_a",
                  "exts": ["rar"],
                  "app": "unrar",
                  "args": "x"
                },
                "tar": {
                  "mode": "archive_a",
                  "exts": ["tar"],
                  "app": "tar",
                  "args": "-xvf"
                },
                "tar_gz": {
                  "mode": "archive_a",
                  "exts": ["tar.gz"],
                  "app": "tar",
                  "args": "-zxvf"
                },
                "tar_xz": {
                  "mode": "archive_b",
                  "exts": ["tar.xz", "txz"],
                  "app": "tar",
                  "args": "--directory FOLDER_PATH -xJf ARCHIVE_PATH"
                }
        ...
        ...
        ...
        },
        "folders": {}
}
```

By default any audio and video files are launched with **mpv**, any image with **sxiv**, any pdf with the **brave** browser, any text with the **atom** editor, etc. But feel free to set your preferred application.

# Examples
For **help**:<br/>
```sh
flauncher -h
or
flauncher --help
```

Launch a **pdf**, a **zip**, a **tar.gz** and a **mp3**:<br/>
```sh
flauncher titi.pdf toto/tutu.zip toto/tutu.tar.gz toto/tata/tutu.mp3
```


# Custom mode
Define others modes corresponding to others conf files with the **-m** parameter.
When specifying the **-m** parameter, you have to precise the **mode** name just after it corresponding to the *~/.config/flauncher/**mode**.json* conf file.
**-m edit** will use the *~/.config/flauncher/edit.json* conf file rather than the default launch.json one.

Then, you can have different launch mode corresponding to any kind of file.


# Suggestions
Use the **o** command to open any file:<br/>
```sh
alias o='flauncher'
```

And the **e** command to edit any file:<br/>
```sh
alias e='flauncher -m edit'
```


# Python import
You can import the flauncher package in your own codes and then call the get_cmds method with the file paths and the mode you want to use.

```
from flauncher import get_cmds
cmds = get_cmds(paths, mode)
```

It will return a list of clean commands, every command being a dictionary with the "app", the "args" and the "su" attributes.
