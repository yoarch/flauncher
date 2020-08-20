import sys
import json
from shutil import copyfile
import os
import subprocess
import ntpath

from .colors import *
from . import log

if __name__ == "__main__":
    logger = log.gen(mode="dev")
else:
    logger = log.gen()

__author__ = 'Yann Orieult'


HOME_PATH = os.environ['HOME']


def _man_inputs(inputs):
    _help_requested(inputs)

    inputs, mode = _man_special_arg(inputs)
    conf_path = HOME_PATH + "/.config/flauncher/" + mode + ".json"

    _man_conf_paths(conf_path, mode)

    if len(inputs) == 0:
        logger.error("needs at least one file to be %sed" % mode)
        exit(1)

    with open(conf_path) as json_f:
        return inputs, json.load(json_f), conf_path


def _help_requested(inputs):
    if len(inputs) == 1 and (inputs[0] == "-h" or inputs[0] == "--help"):
        readme_path = "/usr/lib/flauncher/README.md"
        if not os.path.isfile(readme_path):
            readme_path = os.path.dirname(__file__) + "/conf/README.md"

        f = open(readme_path, 'r')
        print(BLUE + "\n\t#######      flauncher documentation      #######\n" + WHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '').replace('```', '').replace('<pre>', '').replace('</b>', ''). \
                replace('<b>', '').replace('<!-- -->', '').replace('<br/>', '').replace('```sh', ''). \
                replace('***', '').replace('***', '').replace('**', '').replace('*', '')

            print(" " + line, end='')
        print(BASE_C)
        exit(0)


def _man_special_arg(inputs):
    mode = "open"

    if "-m" in inputs:
        m_index = inputs.index("-m")
        if len(inputs) < m_index + 1:
            logger.error("Must enter the wanted mode after the " + WHITE + "-m" + BASE_C + " option\n\t" +
                         "such as \"open\" or \"edit\"")
            exit(1)
        mode = inputs[m_index + 1]
        del inputs[m_index: m_index + 2]

    if "-f" in inputs:
        inputs.remove("-f")

    return inputs, mode


def _man_conf_paths(input_conf_path, mode):
    if not os.path.exists(input_conf_path):

        if os.path.exists(HOME_PATH + "/.config/flauncher/open.json"):
            logger.error(WHITE + "%s" % input_conf_path + BASE_C + "conf path doesn't exist\n\t"
                         "Please create your own conf file from one of the existent in " +
                         WHITE + "%s" % (HOME_PATH + "/.config/flauncher/") + BASE_C)
        else:
            conf_path = None
            if os.path.isfile("/usr/lib/flauncher/open.json"):
                conf_path = "/usr/lib/flauncher/"
            elif os.path.isfile(os.path.dirname(__file__) + "/conf/open.json"):
                conf_path = os.path.dirname(__file__) + "/conf/"

            flauncher_dir_conf_path = HOME_PATH + "/.config/flauncher/"
            if conf_path:
                if not os.path.isdir(flauncher_dir_conf_path):
                    os.mkdir(flauncher_dir_conf_path)
                for file in os.listdir(conf_path):
                    file_path = conf_path + file
                    if file_path.endswith(".json"):
                        copyfile(file_path, flauncher_dir_conf_path + file)
                if mode not in ["open", "edit"]:
                    copyfile(input_conf_path, flauncher_dir_conf_path+ mode + ".json")

            else:
                logger.error("Can not find the conf file " + WHITE + "%s" % input_conf_path + BASE_C + " under " +
                             WHITE + "%s" % flauncher_dir_conf_path + BASE_C +
                             "\nPlease find the conf files in the python archive under \"conf\" and add it under " +
                             WHITE + "%s" % flauncher_dir_conf_path)

                exit(1)


def _run(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.readlines()


def _needs_su(f_path, write=True, read=True, execute=False):
    if write and not os.access(f_path, os.W_OK):
        return True
    if read and not os.access(f_path, os.R_OK):
        return True
    if execute and not os.access(f_path, os.X_OK):
        return True
    return False


def _skipped():
    print(BLUE + "\n\t\t\tskipped\n\n" + BASE_C)


def _get_abs_path(file_paths):
    abs_f_paths = list()
    for file in file_paths:
        abs_f_paths.append(os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(file)))))
    return abs_f_paths


def _is_path_issue(file_path):
    if not os.path.exists(file_path):
        logger.warning("the path " + BLUE + "%s" % file_path + BASE_C + " doesn't exist")
        return True
    elif os.path.isdir(file_path):
        logger.warning("the path " + BLUE + "%s" % file_path + BASE_C + " is a directory, not a file")
        return True
    else:
        return False


def _is_binary(file_path):
    binary = False
    text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_str = lambda bytes: bool(bytes.translate(None, text_chars))
    try:
        if is_binary_str(open(file_path, 'rb').read(1024)):
            binary = True
    finally:
        pass
    return binary


def _create_archive_folder(archive_path, archive_ext, f_type):
    base_path = os.path.dirname(archive_path)
    f_name = os.path.basename(archive_path)

    folder_name = f_name[:-(len(archive_ext) + 1)]

    folder_path = base_path + "/" + folder_name

    if os.path.exists(folder_path):
        folder_path = _find_available_path(base_path, folder_name, f_type)

    try:
        os.mkdir(folder_path)
    except OSError:
        logger.error("creation of the directory " + BLUE + "%s" + BASE_C + " failed" % folder_path)
        folder_path = None

    return folder_path


def _print_cmd(cmd):
    print(WHITE + "\n\t%s\n\n" % cmd + BASE_C, end='')


def _find_available_path(base_path, folder_name, f_type):
    folder_archive_path = base_path + "/" + folder_name + "_" + f_type
    ref_folder_archive_path = folder_archive_path
    if os.path.exists(folder_archive_path):
        folder_archive_path = ref_folder_archive_path + "_archive"
        if os.path.exists(folder_archive_path):
            for i in range(20):
                folder_archive_path = ref_folder_archive_path + "_" + str(i + 1)
                if not os.path.exists(folder_archive_path):
                    break
    return folder_archive_path


def _get_playlist_vs_ext(f_path, conf, f_type, f_needs_su):
    f_names_local_same_ext = list()
    folder_path = os.path.dirname(f_path)

    entered_f_name = os.path.basename(f_path)

    for f_name in os.listdir(folder_path):
        for ext in conf[f_type]["exts"]:
            f_path = folder_path + "/" + f_name
            if f_name.lower().endswith(ext):
                if _needs_su(f_path) == f_needs_su:
                    f_names_local_same_ext.append(f_name)
                break

    f_names_local_same_ext = _sort_str_list(f_names_local_same_ext)
    index_targeted_f = f_names_local_same_ext.index(entered_f_name)
    f_names_same_ext_sorted = f_names_local_same_ext[index_targeted_f:] + f_names_local_same_ext[:index_targeted_f]

    return [folder_path + "/" + f_name for f_name in f_names_same_ext_sorted]


def _sort_str_list(l):
    full_num_elements = list()
    num_elements = list()
    str_elements = list()
    for element in l:
        base_name = element.split(".")[0]
        if _str_is_int(base_name):
            num_elements.append(int(base_name))
            full_num_elements.append(element)
        else:
            str_elements.append(element)

    full_num_elements = [x for _, x in sorted(zip(num_elements, full_num_elements))]
    str_elements.sort()
    return full_num_elements + str_elements


def _str_is_int(str_var):
    try:
        int(str_var)
        return True
    except ValueError:
        return False


# def _run_archive_a_f(conf, f_type, f_paths_sorted_by_f_type):
#     for archive_path in f_paths_sorted_by_f_type[f_type]:
#         cmd = conf[f_type]["cmd"] + " \"" + archive_path + "\""
#         if _needs_su(archive_path):
#             cmd = "sudo " + cmd
#         _print_cmd(cmd)
#         _run(cmd)
#
#
# def _run_archive_b_f(conf, f_type, f_paths_sorted_by_f_type, conf_path):
#     if len(conf[f_type]["exts"]) != 1:
#         logger.error("an archive type can only have one extension, got %s" % conf[f_type]["exts"] +
#                      "extensions\nplease review your launcher conf file located in " + BLUE + "%s" + BASE_C % conf_path)
#         return
#
#     for archive_path in f_paths_sorted_by_f_type[f_type]:
#         folder_path = _create_archive_folder(archive_path, conf[f_type]["exts"][0], f_type)
#         if not folder_path:
#             logger.warning("skipping the %s archive" % archive_path)
#             continue
#
#         cmd_pattern = conf[f_type]["cmd"]
#         cmd = cmd_pattern.replace("FOLDER_PATH", folder_path)
#         cmd = cmd.replace("ARCHIVE_PATH", archive_path)
#         if _needs_su(archive_path):
#             cmd = "sudo " + cmd
#         _print_cmd(cmd)
#         _run(cmd)


def _f_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def _append_to_text(f_paths_sorted_by_f_type, f_path):
    if "text" not in f_paths_sorted_by_f_type:
        f_paths_sorted_by_f_type["text"] = list()
    f_paths_sorted_by_f_type["text"].append(f_path)


def _sort_f_by_ext(f_path, f_paths_sorted_by_f_type, conf):
    f_name = _f_name(f_path).lower()

    if f_name.count('.') == 0 or (f_name.startswith('.') and f_name.count('.') == 1):
        if _is_binary(f_path):
            logger.warning("file " + BLUE + "%s" % f_path + BASE_C + "is considered as text but is binary")
            _skipped()
        else:
            _append_to_text(f_paths_sorted_by_f_type, f_path)
        return

    for f_type, info in conf.items():
        for ext in info["exts"]:

            if f_name.endswith(ext):
                if f_type not in f_paths_sorted_by_f_type:
                    f_paths_sorted_by_f_type[f_type] = list()
                f_paths_sorted_by_f_type[f_type].append(f_path)
                return

    if _is_binary(f_path):
        logger.warning("file " + BLUE + "%s" % f_path + BASE_C + " could not be treated, " +
                       "its extension is unknown from the conf file")
    else:
        _append_to_text(f_paths_sorted_by_f_type, f_path)


def sort_files_by_ext(f_paths, conf):
    f_paths_by_exts = dict()
    for f_path in f_paths:

        if _is_path_issue(f_path):
            continue

        _sort_f_by_ext(f_path, f_paths_by_exts, conf)
    return f_paths_by_exts


def _get_cmds(conf, f_paths_by_exts):

    cmds = list()

    for f_type, f_paths in f_paths_by_exts.items():
        cmd = {"app": conf[f_type]["app"]}

        if conf[f_type]["type"] == "playlist" and len(f_paths) == 1:
            f_needs_su = _needs_su(f_paths[0])
            f_paths = _get_playlist_vs_ext(f_paths[0], conf, f_type, f_needs_su)
            if conf[f_type]["args"]:
                cmd["args"] = conf[f_type]["args"] + ' ' + ' '.join(f_paths)
            else:
                cmd["args"] = ' '.join(f_paths)
            cmd["su"] = f_needs_su
            cmds.append(cmd)

        elif conf[f_type]["type"] == "playlist" or conf[f_type]["type"] == "lonely":
            f_paths_no_su, f_paths_su = list(), list()

            for f_path in f_paths:
                if _needs_su(f_path):
                    f_paths_su.append(f_path)
                else:
                    f_paths_no_su.append(f_path)

            if f_paths_no_su:
                if conf[f_type]["args"]:
                    cmd["args"] = conf[f_type]["args"] + ' ' + ' '.join(f_paths_no_su)
                else:
                    cmd["args"] = ' '.join(f_paths_no_su)
                cmd["su"] = False
                cmds.append(cmd)
            if f_paths_su:
                if conf[f_type]["args"]:
                    cmd["args"] = conf[f_type]["args"] + ' ' + ' '.join(f_paths_su)
                else:
                    cmd["args"] = ' '.join(f_paths_su)
                cmd["su"] = True
                cmds.append(cmd)

        if conf[f_type]["type"] == "archive_a":
            for archive_path in f_paths:
                if conf[f_type]["args"]:
                    cmd["args"] = conf[f_type]["args"] + ' ' + archive_path
                else:
                    cmd["args"] = archive_path
                cmd["su"] = _needs_su(archive_path)
                cmds.append(cmd)

        if conf[f_type]["type"] == "archive_b":
            if len(conf[f_type]["exts"]) != 1:
                logger.error("An archive type can only have one extension, got %s" % conf[f_type]["exts"] +
                             "extensions\nPlease review your launcher conf file")
                continue

            for archive_path in f_paths:
                folder_path = _create_archive_folder(archive_path, conf[f_type]["exts"][0], f_type)
                if not folder_path:
                    logger.warning("Skipping the %s archive" % archive_path)
                    continue

                cmd_pattern = conf[f_type]["args"]
                cmd_pattern = cmd_pattern.replace("FOLDER_PATH", folder_path)
                cmd["args"] = cmd_pattern.replace("ARCHIVE_PATH", archive_path)
                cmd["su"] = _needs_su(archive_path)
                cmds.append(cmd)
    return cmds


def run_cmds(cmds):
    for cmd in cmds:
        built_cmd = cmd["app"] + " " + cmd["args"]
        if cmd["su"]:
            built_cmd = "sudo " + built_cmd

        _print_cmd(built_cmd)
        _run(built_cmd)


def get_cmds(f_paths, mode):

    conf_path = HOME_PATH + "/.config/flauncher/" + mode + ".json"
    _man_conf_paths(conf_path, mode)

    with open(conf_path) as json_f:
        conf = json.load(json_f)

    f_paths = _get_abs_path(f_paths)

    f_paths_by_exts = sort_files_by_ext(f_paths, conf)
    cmds = _get_cmds(conf, f_paths_by_exts)
    return cmds


def launch():
    f_paths, conf, conf_path = _man_inputs(sys.argv[1:])
    f_paths = _get_abs_path(f_paths)

    f_paths_by_exts = sort_files_by_ext(f_paths, conf)
    cmds = _get_cmds(conf, f_paths_by_exts)
    run_cmds(cmds)


if __name__ == "__main__":
    launch()
