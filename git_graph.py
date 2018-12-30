import collections
import os
import re

import pathlib

import git_functions as gf


def get_git_remote_servers(path):
    result = collections.defaultdict(list)
    if pathlib.Path(path + '/.git/refs/remotes/').is_dir():
        for each_folder in os.listdir(path + '/.git/refs/remotes/'):
            for each_file in os.listdir(path + '/.git/refs/remotes/' + each_folder + '/'):
                result[each_folder].append(each_folder[:2] + '/' + each_file)
    return result


def get_git_remote_branches(path, remote_servers):
    result = collections.defaultdict(list)
    for each_server in remote_servers:
        folder = path + '/.git/refs/remotes/' + each_server + '/'
        for each_file in os.listdir(folder):
            with open(folder + each_file, 'r') as each_file_content:
                if each_file == 'HEAD':
                    line = each_file_content.readline()
                    remote_branch = line[line.rfind('/') + 1:-1]
                    result[each_server[:2] + '/' + each_file].append(each_server[:2] + '/' + remote_branch)
                else:
                    result[each_server[:2] + '/' + each_file].append(each_file_content.read().splitlines()[0])
    return result


def __parse_oneline_content_git_folder(path, folder):
    result = collections.defaultdict(list)
    folder = path + '/.git/' + folder + '/'
    for each_file in os.listdir(folder):
        with open(folder + each_file, 'r') as each_file_content:
            result[each_file].append(each_file_content.read().splitlines()[0])
    return result


def get_git_local_branches(path):
    return __parse_oneline_content_git_folder(path, 'refs/heads')


def get_git_tags(path):
    result = __parse_oneline_content_git_folder(path, 'refs/tags')
    if pathlib.Path(path + '/.git/packed-refs').is_file():
        with open(path + '/.git/packed-refs') as p_refs:
            pattern = '(.*) refs/tags/(.*)'
            for each_line in p_refs.read().splitlines():
                match = re.search(pattern, each_line)
                if match:
                    result[match.group(2)].append(match.group(1))
    return result


def get_git_local_head(path):
    result = collections.defaultdict(list)
    with open(path + '/.git/HEAD', 'r') as head_content:
        line = head_content.readline()
        local_branch = line[line.rfind('/') + 1:-1]
        result['head'].append(local_branch)
    return result


def get_git_trees(path, trees):
    result = collections.defaultdict(list)
    pattern = '(tree|blob) (.+)\t(.+)'
    for each_tree in trees:
        for each_line in gf.read_git_file(path, each_tree):
            match = re.search(pattern, each_line)
            if match:
                result[each_tree].append((match.group(2), match.group(3)))
    return result


def get_git_commits(path, commits):
    result = collections.defaultdict(list)
    pattern = '(tree|parent) (.+)'
    for each_commit in commits:
        for each_line in gf.read_git_file(path, each_commit):
            match = re.search(pattern, each_line)
            if match:
                result[each_commit].append(match.group(2))
    return result


def get_git_annotated_tags(path, annotated_tags):
    result = collections.defaultdict(list)
    pattern = '(object) (.+)'
    for each_annotated_tag in annotated_tags:
        for each_line in gf.read_git_file(path, each_annotated_tag):
            match = re.search(pattern, each_line)
            if match:
                result[each_annotated_tag].append(match.group(2))
    return result


class GitGraph:

    def __init__(self, path):
        self.path = path
        self.blobs = []                                      # b: color #9ccc66 (green)  - point to nothing
        self.trees = collections.defaultdict(list)           # t: color #9f7160 (maroon) - point to 0 to N blobs and 0 to N trees
        self.commits = collections.defaultdict(list)         # c: color #b3e5fc (blue)   - point to 1 tree and 0 to N commits
        self.local_branches = collections.defaultdict(list)  # l: color #ffc61a (yellow) - point to 1 commit
        self.local_head = collections.defaultdict(list)      # h: color #cc99ff (violet) - point to 1 local_branch
        self.remote_servers = collections.defaultdict(list)  # s: color #ff9988 (salmon) - point to 1 to N remote_branches
        self.remote_branches = collections.defaultdict(list) # r: color #ff6666 (red)    - point to 1 commit
        self.remote_heads = collections.defaultdict(list)    # d: color #ffa366 (orange) - point to 1 remote branch
        self.annotated_tags = collections.defaultdict(list)  # a: color #00cc99 (turquo) - point to 1 commit
        self.tags = collections.defaultdict(list)            # g: color #ff66b3 (pink)   - point to 1 commit or 1 annotated_tag
        self.dot_graph = ''

    def build_graph(self):
        self.blobs, trees, commits, annotated_tags = gf.get_git_objects(self.path)
        self.trees = get_git_trees(self.path, trees)
        self.commits = get_git_commits(self.path, commits)
        self.local_branches = get_git_local_branches(self.path)
        self.local_head = get_git_local_head(self.path)
        self.remote_servers = get_git_remote_servers(self.path)
        self.remote_branches = get_git_remote_branches(self.path, self.remote_servers)
#        self.remote_heads = 
        self.tags = get_git_tags(self.path)
        self.annotated_tags = get_git_annotated_tags(self.path, annotated_tags)
        return self
