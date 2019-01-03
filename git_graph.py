import collections
import os
import re

import pathlib

import git_functions as gf


def build_git_remote_servers(remote_branches):
    result = collections.defaultdict(list)
    for rb in remote_branches:
        result[rb[0][:rb[0].find('/')]].append(rb[0][rb[0].find('/') + 1:])
    return result


def build_git_remote_branches(remote_branches):
    result = {}
    for rb in remote_branches:
        result[(rb[0][:rb[0].find('/')], rb[0][rb[0].find('/') + 1:])] = rb[1]
    return result


def get_git_local_branches(path):
    result = {}
    folder = path + '/.git/refs/heads/'
    for each_file in os.listdir(folder):
        with open(folder + each_file, 'r') as each_file_content:
            result[each_file] = (each_file_content.read().splitlines()[0])
    return result


def get_git_tags(path):
    result = {}
    if pathlib.Path(path + '/.git/packed-refs').is_file():
        with open(path + '/.git/packed-refs') as p_refs:
            pattern = '(.*) refs/tags/(.*)'
            for each_line in p_refs.read().splitlines():
                match = re.search(pattern, each_line)
                if match:
                    result[match.group(2)] = match.group(1)
    folder = path + '/.git/refs/tags/'
    for each_file in os.listdir(folder):
        with open(folder + each_file, 'r') as each_file_content:
            result[each_file] = each_file_content.read().splitlines()[0]
    return result


def get_git_local_head(path):
    with open(path + '/.git/HEAD', 'r') as head_content:
        line = head_content.readline()
        local_branch = line[line.rfind('/') + 1:-1]
        result = ('HEAD', local_branch)
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
    result = {}
    pattern = '(object) (.+)'
    for each_annotated_tag in annotated_tags:
        for each_line in gf.read_git_file(path, each_annotated_tag):
            match = re.search(pattern, each_line)
            if match:
                result[each_annotated_tag] = match.group(2)
    return result


class GitGraph:

    def __init__(self, path):
        self.path = path
        self.blobs = []                                      # b: color #9ccc66 (green)  - point to nothing
        self.trees = collections.defaultdict(list)           # t: color #bc9b8f (maroon) - point to 0 to N blobs and 0 to N trees
        self.commits = collections.defaultdict(list)         # c: color #6cccf9 (blue)   - point to 1 tree and 0 to N commits
        self.local_branches = {}                             # l: color #ffc61a (yellow) - point to 1 commit
        self.local_head = ('', '')                           # h: color #cc99ff (violet) - point to 1 local_branch
        self.remote_servers = collections.defaultdict(list)  # s: color #ff9988 (salmon) - point to 1 to N remote_branches
        self.remote_branches = {}                            # r: color #ff6666 (red)    - point to 1 commit
        self.remote_heads = {}                               # d: color #ffa366 (orange) - point to 1 remote branch
        self.annotated_tags = {}                             # a: color #00cc99 (turquo) - point to 1 commit
        self.tags = {}                                       # g: color #ff66b3 (pink)   - point to 1 commit or 1 annotated_tag

    def build_graph(self):
        blobs, trees, commits, annotated_tags = gf.get_git_objects(self.path)
        local_branches, remote_branches, tags = gf.get_git_references(self.path)

        self.blobs = blobs
        self.trees = get_git_trees(self.path, trees)
        self.commits = get_git_commits(self.path, commits)
        self.local_branches = get_git_local_branches(self.path)
        self.local_head = get_git_local_head(self.path)
        self.remote_servers = build_git_remote_servers(remote_branches)
        self.remote_branches = build_git_remote_branches(remote_branches)
#        self.remote_heads = 
        self.tags = get_git_tags(self.path)
        self.annotated_tags = get_git_annotated_tags(self.path, annotated_tags)
        return self
