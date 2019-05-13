import sys
import json
import os
import subprocess
from shutil import copyfile
from os import listdir


CBRED = '\033[38;5;196;1m'
CBORANGE = '\033[38;5;202;1m'
CBGREEN = '\033[38;5;40;1m'
CBYELLOW = '\033[1;33m'
CBWHITE = '\033[1;37m'
CBPURPLE = '\033[1;35m'
CBBLUE = '\033[1;34m'
CBASE = '\033[0m'


def check_help_request(arguments):
    if len(arguments) == 1 and (arguments[0] == "-h" or arguments[0] == "--help"):
        README_path = "/usr/lib/flauncher/README.md"

        f = open(README_path, 'r')
        print(CBBLUE + "\n\t#######      flauncher documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '').replace('```', '').replace('<pre>', '').replace('</b>', '').\
                replace('<b>', '').replace('<!-- -->', '').replace('<br/>', '').replace('```sh', '').\
                replace('***', '').replace('***', '').replace('**', '').replace('*', '')

            print(" " + line, end='')
        print(CBASE)
        exit()


def run(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.readlines()


def OK(msg=""):
    print(CBGREEN + "\n\t[OK] " + CBASE + msg)


def INFO(msg=""):
    print(CBWHITE + "\n\t[INFO] " + CBASE + msg)


def WARNING(msg=""):
    print(CBORANGE + "\n\t[WARNING] " + CBASE + msg)


def ERROR(msg=""):
    print(CBRED + "\n\t[ERROR] " + CBASE + msg)


def skipped():
    print(CBBLUE + "\n\t\t\tskipped\n\n" + CBASE)


def init_fpaths_sorted_by_ftype(ftypes):
    fpaths_sorted_by_ftype = dict()
    for ftype in ftypes:
        fpaths_sorted_by_ftype[ftype] = list()
    return fpaths_sorted_by_ftype


def get_launchers():

    def_launchers_fname = "default_launchers.json"
    perso_launchers_fname = "launchers.json"
    HOME_PATH = os.environ['HOME']
    perso_flauncher_folder_path = HOME_PATH + "/.config/flauncher/"
    perso_flauncher_file_path = perso_flauncher_folder_path + perso_launchers_fname

    create_perso_flauncher_folder(perso_flauncher_folder_path)
    create_perso_flauncher_file(perso_flauncher_file_path, def_launchers_fname)

    with open(perso_flauncher_file_path) as launchers_f:
        return json.load(launchers_f), perso_flauncher_file_path


def create_perso_flauncher_folder(perso_flauncher_folder_path):
    if not os.path.exists(perso_flauncher_folder_path):
        try:
            os.mkdir(perso_flauncher_folder_path)
        except OSError as err_msg:
            ERROR("creation of the directory " + CBBLUE + "%s" % perso_flauncher_folder_path + CBASE + " failed:\n%s" % err_msg)


def create_perso_flauncher_file(perso_flauncher_file_path, def_launchers_fname):
    if not os.path.exists(perso_flauncher_file_path):
        default_launchersconf_path = "/usr/lib/flauncher/" + def_launchers_fname

        INFO("the personal launchers conf path %s doesn't exist\n\n\tcopying the default launchers conf "
             "from %s to %s\n\n\t\tdon't forget to customize the launchers by editing this file"
             % (perso_flauncher_file_path, default_launchersconf_path, perso_flauncher_file_path))

        copyfile(default_launchersconf_path, perso_flauncher_file_path)


def get_abs_path(files):
    abs_fpaths = list()
    for file in files:
        abs_fpaths.append(os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(file)))))
    return abs_fpaths


def check_path_issues(file_path):
    path_issue = True
    if not os.path.exists(file_path):
        WARNING("the path " + CBBLUE + "%s" + CBASE + " doesn't exist" % file_path)
    elif os.path.isdir(file_path):
        WARNING("the path " + CBBLUE + "%s" + CBASE + " is a directory, not a file" % file_path)
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


def generate_folder_from_archive(archive_path, archive_ext, ftype):

    base_path = os.path.dirname(archive_path)
    fname = os.path.basename(archive_path)

    folder_name = fname[:-(len(archive_ext)+1)]

    folder_path = base_path + "/" + folder_name

    if os.path.exists(folder_path):
        folder_path = find_folder_path_not_existing(base_path, folder_name, ftype)

    try:
        os.mkdir(folder_path)
    except OSError:
        ERROR("creation of the directory " + CBBLUE + "%s" + CBASE + " failed" % folder_path)
        folder_path = None

    return folder_path


def check_nb_files(input_files):
    if len(input_files) == 0:
        raise ValueError("need at least one file to launch ...")


def print_cmd(cmd):
    print(CBWHITE + "\n\t%s\n\n" % cmd + CBASE, end='')


def find_folder_path_not_existing(base_path, folder_name, ftype):
    folder_archive_path = base_path + "/" + folder_name + "_" + ftype
    ref_folder_archive_path = folder_archive_path
    if os.path.exists(folder_archive_path):
        folder_archive_path = ref_folder_archive_path + "_archive"
        if os.path.exists(folder_archive_path):
            for i in range(20):
                folder_archive_path = ref_folder_archive_path + "_" + str(i+1)
                if not os.path.exists(folder_archive_path):
                    break
    return folder_archive_path


def launch_cmds(fpaths_sorted_by_ftype, ftype, launchers, launchersconf_path):
    if launchers[ftype]["type"] == "playlist":
        run_playlist_f(launchers, ftype, fpaths_sorted_by_ftype)

    if launchers[ftype]["type"] == "lonely":
        run_lonely_f(launchers, ftype, fpaths_sorted_by_ftype)

    if launchers[ftype]["type"] == "archive_a":
        run_archive_a_f(launchers, ftype, fpaths_sorted_by_ftype)

    if launchers[ftype]["type"] == "archive_b":
        run_archive_b_f(launchers, ftype, fpaths_sorted_by_ftype, launchersconf_path)


def run_playlist_f(launchers, ftype, fpaths_sorted_by_ftype):
    app_cmd = launchers[ftype]["cmd"]

    fpaths = fpaths_sorted_by_ftype[ftype]
    if len(fpaths) == 1:
        fpaths = get_playlist_fpaths_same_ftype(fpaths[0], launchers, ftype)

    cmd = app_cmd + " \"" + '\" \"'.join(fpaths) + "\""
    print_cmd(cmd)
    run(cmd)


def get_playlist_fpaths_same_ftype(lonely_fpath, launchers, ftype):

    fnames_same_ftype = list()
    folder_path_lonely_f = os.path.dirname(lonely_fpath)
    lonely_fname = os.path.basename(lonely_fpath)

    for fname in listdir(folder_path_lonely_f):
        for ext in launchers[ftype]["exts"]:
            if fname.endswith(ext) and os.path.isfile(folder_path_lonely_f + "/" + fname):
                fnames_same_ftype.append(fname)
                break

    fnames_same_ftype.sort()
    pos_targeted_f = fnames_same_ftype.index(lonely_fname)
    fnames_same_ftype_sorted = fnames_same_ftype[pos_targeted_f:] + fnames_same_ftype[:pos_targeted_f]
    playlist_fpaths = [folder_path_lonely_f + "/" + fname_same_ftype for fname_same_ftype in fnames_same_ftype_sorted]
    return playlist_fpaths


def run_lonely_f(launchers, ftype, fpaths_sorted_by_ftype):
    app_cmd = launchers[ftype]["cmd"]

    fpaths = fpaths_sorted_by_ftype[ftype]

    cmd = app_cmd + " \"" + '\" \"'.join(fpaths) + "\""
    print_cmd(cmd)
    run(cmd)


def run_archive_a_f(launchers, ftype, fpaths_sorted_by_ftype):
    for archive_path in fpaths_sorted_by_ftype[ftype]:
        cmd = launchers[ftype]["cmd"] + " \"" + archive_path + "\""
        print_cmd(cmd)
        run(cmd)


def run_archive_b_f(launchers, ftype, fpaths_sorted_by_ftype, launchersconf_path):

    if len(launchers[ftype]["exts"]) != 1:
        ERROR("an archive type can only have one extension, got %s" % launchers[ftype]["exts"] + "extensions\n"
              "please review your launcher conf file located in " + CBBLUE + "%s" + CBASE % launchersconf_path)
        return

    for archive_path in fpaths_sorted_by_ftype[ftype]:
        folder_path = generate_folder_from_archive(archive_path, launchers[ftype]["exts"][0], ftype)
        if not folder_path:
            WARNING("skipping the %s archive" % archive_path)
            continue

        cmd_pattern = launchers[ftype]["cmd"]
        cmd = cmd_pattern.replace("FOLDER_PATH", folder_path)
        cmd = cmd.replace("ARCHIVE_PATH", archive_path)
        print_cmd(cmd)
        run(cmd)


def get_ftypes(launchers):
    ftypes = list()
    for ftype in launchers:
        ftypes.append(ftype)
    return ftypes


def route_fpaths_by_ext(fpath, fpaths_sorted_by_ftype, launchers):
    for ftype_key, ftype_value in launchers.items():
        for ext in ftype_value["exts"]:
            if fpath.lower().endswith("." + ext.lower()):
                fpaths_sorted_by_ftype[ftype_key].append(fpath)
                return

    if not check_binary(fpath):
        fpaths_sorted_by_ftype["text"].append(fpath)


def main():

    input_parms = sys.argv[1:]
    check_help_request(input_parms)
    check_nb_files(input_parms)
    fpaths = get_abs_path(input_parms)

    launchers, launchersconf_path = get_launchers()
    ftypes = get_ftypes(launchers)
    fpaths_sorted_by_ftype = init_fpaths_sorted_by_ftype(ftypes)

    for fpath in fpaths:

        if check_path_issues(fpath):
            continue

        route_fpaths_by_ext(fpath, fpaths_sorted_by_ftype, launchers)

    for ftype in ftypes:
        if len(fpaths_sorted_by_ftype[ftype]) > 0:
            launch_cmds(fpaths_sorted_by_ftype, ftype, launchers, launchersconf_path)


if __name__ == "__main__":
    main()
