# flauncher
universal file launcher for terminal

Launch any file in terminal with one unique command. flauncher works as a command router and launches the entered files with the according application regarding your preferences settings.

flauncher deals with **audio, image, pdf, rar, tar, tar.gz, tar.xz, tar.bz2, text, tgz, zip and video** files.

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


# examples
for help:<br/>
```sh
flauncher -h
or
flauncher --help
```

opens a pdf, a zip, a tar.gz and a mp3:<br/>
```sh
flauncher titi.pdf toto/tutu.zip toto/tutu.tar.gz toto/tata/tutu.mp3
```

# suggestions
use the **o** command to open any file:<br/>
```sh
alias o='flauncher'
```
