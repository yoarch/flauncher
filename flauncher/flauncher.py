import sys
import json
import os
import subprocess
from shutil import copyfile

import logging
# from .logger import build_logger
from logger import build_logger
logger = build_logger("flauncher", level=logging.INFO)


CRED = '\033[31m'
CBYELLOW = '\033[1;33m'
CBWHITE = '\033[1;37m'
CBPURPLE = '\033[1;35m'
CBBLUE = '\033[1;34m'
CNORMAL_WHITE = '\033[0m'

COCCURRENCES = CBPURPLE
CFILE_PATHS = CBBLUE
CTEXT_FILES = CBWHITE


def check_help_request(arguments):
    if len(arguments) == 1 and (arguments[0] == "-h" or arguments[0] == "--help"):
        README_path = "/usr/lib/modfname/README.md"

        f = open(README_path, 'r')
        print(CFILE_PATHS + "\n\t#######      modfname documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '')
            line = line.replace('```', '')
            line = line.replace('<pre>', '')
            line = line.replace('</b>', '')
            line = line.replace('<b>', '')
            line = line.replace('<!-- -->', '')
            line = line.replace('<br/>', '')
            line = line.replace('```sh', '')
            line = line.replace('***', '')
            line = line.replace('**', '')
            line = line.replace('*', '')
            print(" " + line, end='')
        print(CNORMAL_WHITE)
        exit()


def run(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.readlines()


def init_fdata():

    file_data = {
        "audio": {"nb": 0, "file_paths": list()},
        "image": {"nb": 0, "file_paths": list()},
        "pdf": {"nb": 0, "file_paths": list()},
        "rar": {"nb": 0, "file_paths": list()},
        "tar": {"nb": 0, "file_paths": list()},
        "tar_gz": {"nb": 0, "file_paths": list()},
        "tar_xz": {"nb": 0, "file_paths": list()},
        "tar_bz2": {"nb": 0, "file_paths": list()},
        "text": {"nb": 0, "file_paths": list()},
        "tgz": {"nb": 0, "file_paths": list()},
        "zip": {"nb": 0, "file_paths": list()},
        "video": {"nb": 0, "file_paths": list()}
    }
    return file_data


def get_launchers():

    default_launchersconf_name = "default_launchers.json"
    perso_launchersconf_name = "launchers.json"
    HOME_PATH = os.environ['HOME']
    perso_launchersconf_path = HOME_PATH + "/.config/flauncher/" + perso_launchersconf_name

    if not os.path.exists(perso_launchersconf_path):
        default_launchersconf_path = "/usr/lib/flauncher/" + default_launchersconf_name
        logger.info("the personal launchers conf path %s doesn't exist\n\tcopying the default launchers conf from %s "
                    "to %s\n\t\tdon't forget to customize the launchers by editing "
                    "this file" % (perso_launchersconf_path, default_launchersconf_path, perso_launchersconf_path))
        copyfile(default_launchersconf_path, perso_launchersconf_path)

    with open(perso_launchersconf_path) as f:
        return json.load(f)


def get_abs_path(files):
    abs_file_paths = list()
    for file in files:
        # abs_file_paths.append(os.path.abspath(file))
        abs_file_paths.append(os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(file)))))
    return abs_file_paths


def check_path_issues(file_path):
    path_issue = True
    if not os.path.exists(file_path):
        logger.warning("the path %s doesn't exist" % file_path)
    elif os.path.isdir(file_path):
        logger.warning("the path %s is a directory, not a file" % file_path)
    else:
        path_issue = False
    return path_issue


def check_binary(file_path):
    is_binary = False
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    try:
        if is_binary_string(open(file_path, 'rb').read(1024)):
            is_binary = True
    except:
        pass
    return is_binary


def get_media_exts():
    audio_exts = json.load(open("/usr/lib/flauncher/audio_exts.json"))
    image_exts = json.load(open("/usr/lib/flauncher/image_exts.json"))
    video_exts = json.load(open("/usr/lib/flauncher/video_exts.json"))
    return audio_exts, image_exts, video_exts


def file_router_one_ext(f, filepath, ext, audio_exts, image_exts, video_exts):

    for audio_ext in audio_exts:
        if ext == audio_ext:
            f["audio"]["nb"] += 1
            f["audio"]["file_paths"].append(filepath)
            return

    for image_ext in image_exts:
        if ext == image_ext:
            f["image"]["nb"] += 1
            f["image"]["file_paths"].append(filepath)
            return

    for video_ext in video_exts:
        if ext == video_ext:
            f["video"]["nb"] += 1
            f["video"]["file_paths"].append(filepath)
            return

    if ext == "pdf":
        f["pdf"]["nb"] += 1
        f["pdf"]["file_paths"].append(filepath)

    elif ext == "rar":
        f["rar"]["nb"] += 1
        f["rar"]["file_paths"].append(filepath)

    elif ext == "tar":
        f["tar"]["nb"] += 1
        f["tar"]["file_paths"].append(filepath)

    elif ext == "tgz":
        f["tgz"]["nb"] += 1
        f["tgz"]["file_paths"].append(filepath)

    elif ext == "zip":
        f["zip"]["nb"] += 1
        f["zip"]["file_paths"].append(filepath)

    else:
        if not check_binary(filepath):
            f["text"]["nb"] += 1
            f["text"]["file_paths"].append(filepath)


def file_router_two_exts(f, filepath, ext):

    found = True
    if ext == "tar.gz":
        f["tar_gz"]["nb"] += 1
        f["tar_gz"]["file_paths"].append(filepath)

    elif ext == "tar.xz":
        f["tar_xz"]["nb"] += 1
        f["tar_xz"]["file_paths"].append(filepath)

    elif ext == "tar.bz2":
        f["tar_bz2"]["nb"] += 1
        f["tar_bz2"]["file_paths"].append(filepath)
    else:
        found = False
    return found


def main():

    input_parms = sys.argv[1:]

    check_help_request(input_parms)

    launchers = get_launchers()

    filepaths = get_abs_path(input_parms)
    file_types = ["audio", "image", "pdf", "rar", "tar", "tar_gz", "tar_xz", "tar_bz2", "text", "tgz", "zip", "video"]

    if len(filepaths) == 0:
        raise ValueError("need at least one file to open ...")

    audio_exts, image_exts, video_exts = get_media_exts()

    f = init_fdata()

    for filepath in filepaths:

        if check_path_issues(filepath):
            continue

        fname = os.path.basename(filepath)
        nb_dot = fname.count('.')
        if nb_dot == 0:
            if not check_binary(filepath):
                f["text"]["nb"] += 1
                f["text"]["file_paths"].append(filepath)
        elif nb_dot == 1:
            ext = fname.split('.')[-1]
            file_router_one_ext(f, filepath, ext.lower(), audio_exts, image_exts, video_exts)
        else:
            ext = fname.split('.')[-2] + '.' + fname.split('.')[-1]
            found = file_router_two_exts(f, filepath, ext.lower())
            if not found:
                file_router_one_ext(f, filepath, ext.lower(), audio_exts, image_exts, video_exts)

    for file_type in file_types:
        if f[file_type]["nb"] > 0:
            run(launchers[file_type] + " \"" + '\" \"'.join(f[file_type]["file_paths"]) + "\"")


if __name__ == "__main__":
    main()
