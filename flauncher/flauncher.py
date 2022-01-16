import sys
import json
from shutil import copyfile
import os
import subprocess
import ntpath
from natsort import natsorted

from .colors import *
from . import log
logger = log.gen()

__author__ = 'Yann Orieult'


FLAUNCHER_DIR_CONF = os.environ['HOME'] + "/.config/flauncher/"


def _man_inputs(inputs):
    _help_requested(inputs)

    inputs, mode = _man_special_arg(inputs)
    conf_path = FLAUNCHER_DIR_CONF + mode + ".json"

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

        if os.path.exists(FLAUNCHER_DIR_CONF + "open.json"):
            logger.error(WHITE + "%s" % input_conf_path + BASE_C + "conf path doesn't exist\n\t"
                         "Please create your own conf file from one of the existent in " +
                         WHITE + "%s" % FLAUNCHER_DIR_CONF + BASE_C)
        else:
            conf_path = None
            if os.path.isfile("/usr/lib/flauncher/open.json"):
                conf_path = "/usr/lib/flauncher/"
            elif os.path.isfile(os.path.dirname(__file__) + "/conf/open.json"):
                conf_path = os.path.dirname(__file__) + "/conf/"

            if conf_path:
                if not os.path.isdir(FLAUNCHER_DIR_CONF):
                    os.mkdir(FLAUNCHER_DIR_CONF)
                for file in os.listdir(conf_path):
                    file_path = conf_path + file
                    if file_path.endswith(".json"):
                        copyfile(file_path, FLAUNCHER_DIR_CONF + file)
                if mode not in ["open", "edit"]:
                    copyfile(input_conf_path, FLAUNCHER_DIR_CONF + mode + ".json")

            else:
                logger.error("Can not find the conf file " + WHITE + "%s" % input_conf_path + BASE_C + " under " +
                             WHITE + "%s" % FLAUNCHER_DIR_CONF + BASE_C +
                             "\nPlease find the conf files in the python archive under \"conf\" and add it under " +
                             WHITE + "%s" % FLAUNCHER_DIR_CONF)

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


# def _sort_str_list(l):
#     full_num_elements = list()
#     num_elements = list()
#     str_elements = list()
#     for element in l:
#         base_name = element.split(".")[0]
#         if _str_is_int(base_name):
#             num_elements.append(int(base_name))
#             full_num_elements.append(element)
#         else:
#             str_elements.append(element)
#
#     full_num_elements = [x for _, x in sorted(zip(num_elements, full_num_elements))]
#     str_elements.sort()
#     return full_num_elements + str_elements


def _str_is_int(str_var):
    try:
        int(str_var)
        return True
    except ValueError:
        return False


def _f_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def _append_to_text(f_paths_sorted_by_f_type, f_path):
    if "text" not in f_paths_sorted_by_f_type:
        f_paths_sorted_by_f_type["text"] = list()
    f_paths_sorted_by_f_type["text"].append(f_path)


def sort_paths_by_exts(paths):

    files_paths, folders_paths = list(), list()

    for f_path in paths:

        if _is_path_issue(f_path):
            continue

        if os.path.isfile(f_path):
            files_paths.append(f_path)
        elif os.path.isdir(f_path):
            folders_paths.append(f_path)

    files_by_exts = dict()
    files_exts_set = set()

    for file_path in files_paths:
        files_exts_set.add(os.path.splitext(file_path)[1].replace('.', ''))

    for file_ext in files_exts_set:
        files_by_exts[file_ext] = list()

    for file_path in files_paths:
        files_by_exts[os.path.splitext(file_path)[1].replace('.', '')].append(file_path)

    if '' in files_by_exts:
        no_binary_text_files = files_by_exts[''].copy()
        for text_file_path in files_by_exts['']:
            if _is_binary(text_file_path):
                logger.warning(f"File {BLUE}{text_file_path}{BASE_C} is binary")
                no_binary_text_files.remove(text_file_path)

        files_by_exts[''] = no_binary_text_files


    folders_by_exts = dict()
    folders_exts_set = set()

    for folder_path in folders_paths:
        folders_exts_set.add(os.path.splitext(folder_path)[1].replace('.', ''))

    for folder_ext in folders_exts_set:
        folders_by_exts[folder_ext] = list()

    for folder_path in folders_paths:
        folders_by_exts[os.path.splitext(folder_path)[1].replace('.', '')].append(folder_path)

    return {
        "files": files_by_exts,
        "folders": folders_by_exts
    }


def _get_all_having_same_type_in_folder(f_path, exts, f_needs_su):
    f_with_same_type = list()
    folder_path = os.path.dirname(f_path)

    entered_f_name = os.path.basename(f_path)

    for f_name in os.listdir(folder_path):
        for ext in exts:
            f_path = folder_path + "/" + f_name
            if f_name.lower().endswith(ext):
                if _needs_su(f_path) == f_needs_su:
                    f_with_same_type.append(f_name)
                break

    f_with_same_type = natsorted(f_with_same_type, key=lambda y: y.lower())

    index_targeted_f = f_with_same_type.index(entered_f_name)
    f_names_same_ext_sorted = f_with_same_type[index_targeted_f:] + f_with_same_type[:index_targeted_f]

    return [folder_path + "/" + f_name for f_name in f_names_same_ext_sorted]


def _build_dict_cmds(paths_to_launch):

    cmds = list()

    for fs_type in ["files", "folders"]:

        for type, params in paths_to_launch[fs_type].items():

            if params["mode"] == "playlist" and len(params["paths"]) == 1:

                f_with_same_type_in_folder = _get_all_having_same_type_in_folder(params["paths"][0],
                                                                                 params["exts"],
                                                                                 _needs_su(params["paths"][0]))

                args = params["args"] + ' ' + ' '.join(f_with_same_type_in_folder) if params["args"]\
                    else ' '.join(f_with_same_type_in_folder)

                cmds.append(
                    {
                        "app": params["app"],
                        "args": args,
                        "su": _needs_su(params["paths"][0])
                    }
                )

            elif params["mode"] in ["playlist", "individual"]:

                args = params["args"] + ' ' + ' '.join(_get_paths_str(natsorted(params["paths"],
                                                                                key=lambda y: y.lower())))\
                    if params["args"] else\
                    ' '.join(_get_paths_str(natsorted(params["paths"], key=lambda y: y.lower())))

                cmds.append(
                    {
                        "app": params["app"],
                        "args": args,
                        "su": _needs_su(params["paths"][0])
                    }
                )

            elif params["mode"] == "archive_a":
                for archive_path in params["paths"]:
                    args = params["args"] + ' ' + _add_quotes_path(archive_path) if params["args"]\
                        else _add_quotes_path(archive_path)

                    cmds.append(
                        {
                            "app": params["app"],
                            "args": args,
                            "su": _needs_su(archive_path)
                        }
                    )

            if params["mode"] == "archive_b":

                for archive_path in params["paths"]:
                    folder_path = _create_archive_folder(_add_quotes_path(archive_path), params["exts"][0],
                                                         params["mode"])
                    cmd_pattern = params["args"]
                    cmd_pattern = cmd_pattern.replace("FOLDER_PATH", folder_path)

                    cmds.append(
                        {
                            "app": params["app"],
                            "args": cmd_pattern.replace("ARCHIVE_PATH", _add_quotes_path(archive_path)),
                            "su": _needs_su(archive_path)
                        }
                    )
    logger.debug(f"Built commands: {cmds}")
    return cmds


def _get_paths_str(paths):
    paths_str = list()
    for path in paths:
        paths_str.append(_add_quotes_path(path))
    return paths_str


def _add_quotes_path(path):
    if " " in path or "'" in path:
        return "\"" + path + "\""
    return path


def run_cmds(cmds):
    for cmd in cmds:
        built_cmd = cmd["app"] + " " + cmd["args"]
        display_cmd = ORANGE + cmd["app"] + BASE_C + " " + cmd["args"]
        if cmd["su"]:
            built_cmd = "sudo " + built_cmd
            display_cmd = RED + "sudo " + display_cmd

        logger.info(display_cmd)
        _run(built_cmd)


def _paths_to_launch_by_type(sorted_paths_by_exts, conf):

    files_to_launch = dict()
    for ext, files_list in sorted_paths_by_exts["files"].items():
        for file_type, file_params in conf["files"].items():
            if ext in file_params["exts"]:
                if not file_type in files_to_launch:
                    files_to_launch[file_type] = file_params
                    files_to_launch[file_type]["paths"] = list()
                files_to_launch[file_type]["paths"] += files_list
                break

    logger.debug(f"Files to launch: {files_to_launch}")

    folders_to_launch = dict()
    for ext, folders_list in sorted_paths_by_exts["folders"].items():
        for folder_type, folder_params in conf["folders"].items():
            if ext in folder_params["exts"]:
                if not folder_type in folders_to_launch:
                    folders_to_launch[folder_type] = folder_params
                    folders_to_launch[folder_type]["paths"] = list()
                folders_to_launch[folder_type]["paths"] += folders_list
                break

    logger.debug(f"Folders to launch: {folders_to_launch}")

    return {
        "files": files_to_launch,
        "folders": folders_to_launch
    }


def get_cmds(paths, mode):

    conf_path = f"{FLAUNCHER_DIR_CONF}{mode}.json"
    _man_conf_paths(conf_path, mode)

    json_conf_file = open(conf_path)
    conf = json.load(json_conf_file)
    json_conf_file.close()
    logger.debug(f"Conf: {conf}")

    paths = _get_abs_path(paths)
    sorted_paths_by_exts = sort_paths_by_exts(paths)
    logger.debug(f"sorted paths by exts: {sorted_paths_by_exts}")

    return _build_dict_cmds(_paths_to_launch_by_type(sorted_paths_by_exts, conf))


def launch():
    paths, conf, conf_path = _man_inputs(sys.argv[1:])
    paths = _get_abs_path(paths)

    sorted_paths_by_exts = sort_paths_by_exts(paths)
    run_cmds(_build_dict_cmds(_paths_to_launch_by_type(sorted_paths_by_exts, conf)))


if __name__ == "__main__":
    launch()
