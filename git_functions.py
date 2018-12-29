import os
import pathlib
import subprocess


def _is_git_repository(path):
    is_repo = pathlib.Path(path + '/.git').is_dir()
    if not is_repo:
        print('Not a git repository')
    return is_repo


def get_git_object_files(path):
    if not _is_git_repository(path):
        return None
    result = []
    for each_dir in os.listdir(path + '/.git/objects/'):
        if each_dir != 'info' and each_dir != 'pack':
            for each_file in os.listdir(path + '/.git/objects/' + each_dir + '/'):
                result.append(each_dir + each_file)
    return result


def get_git_file_type(path, sha1_file):
    if not _is_git_repository(path):
        return None
    bashCommand = 'git -C ' + path + ' cat-file -t ' + sha1_file
    output, error = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    if output:
        output = output.decode('utf-8')
        return output.splitlines()[0]


def read_git_file(path, sha1_file):
    if not _is_git_repository(path):
        return None
    bashCommand = 'git -C ' + path + ' cat-file -p ' + sha1_file
    output, error = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    if output:
        output = output.decode('utf-8')
        return output.splitlines()


def get_git_objects(path):
    blobs = []
    trees = []
    commits = []
    annotated_tags = []
    for each_git_file in get_git_object_files(path):
        git_file_type = get_git_file_type(path, each_git_file)
        if git_file_type == 'blob':
            blobs.append(each_git_file)
        if git_file_type == 'tree':
            trees.append(each_git_file)
        if git_file_type == 'commit':
            commits.append(each_git_file)
        if git_file_type == 'tag':
            annotated_tags.append(each_git_file)
    return blobs, trees, commits, annotated_tags

