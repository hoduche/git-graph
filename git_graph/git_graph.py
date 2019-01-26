import collections as c
import re

import git_graph.git_functions as gf


def build_git_trees(path, trees):
    result = c.defaultdict(list)
    pattern = '(tree|blob) (.+)\t(.+)'
    for each_tree in trees:
        for each_line in gf.read_git_file(path, each_tree):
            match = re.search(pattern, each_line)
            if match:
                result[each_tree].append((match.group(2), match.group(3)))
    return result


def build_git_commits(path, commits):
    result = c.defaultdict(list)
    pattern = '(tree|parent) (.+)'
    for each_commit in commits:
        for each_line in gf.read_git_file(path, each_commit):
            match = re.search(pattern, each_line)
            if match:
                result[each_commit].append(match.group(2))
    return result


def build_git_remote_servers(remote_branches, remote_heads):
    result = c.defaultdict(list)
    for rb in remote_branches:
        server = rb[:rb.find('/')]
        result[server].append(rb)
    for rb in remote_heads:
        server = rb[:rb.find('/')]
        result[server].append(rb)
    return result


def build_git_annotated_tags(path, annotated_tags):
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
        self.blobs = []                            # b: -> nothing
        self.trees = c.defaultdict(list)           # t: -> 0 to N blobs and 0 to N trees
        self.commits = c.defaultdict(list)         # c: -> 1 tree and 0 to N commits
        self.local_branches = {}                   # l: -> 1 commit
        self.local_head = ('', '')                 # h: -> 1 local_branch
        self.remote_branches = {}                  # r: -> 1 commit
        self.remote_heads = {}                     # d: -> 1 remote branch
        self.remote_servers = c.defaultdict(list)  # s: -> 1 to N remote_branches
        self.annotated_tags = {}                   # a: -> 1 commit
        self.tags = {}                             # g: -> 1 commit or 1 annotated_tag
        self.upstreams = {}                        # u: -> 1 local_branch

    def build_graph(self):
        blobs, trees, commits, annotated_tags = gf.get_git_objects(self.path)
        local_branches, remote_branches, tags = gf.get_git_references(self.path)
        local_head = gf.get_git_local_head(self.path)
        remote_heads = gf.get_git_remote_heads(self.path)
        upstreams = gf.get_git_upstreams(self.path)

        self.blobs = blobs
        self.trees = build_git_trees(self.path, trees)
        self.commits = build_git_commits(self.path, commits)
        self.local_branches = local_branches
        self.local_head = ('HEAD', local_head)
        self.remote_branches = remote_branches
        self.remote_heads = remote_heads
        self.remote_servers = build_git_remote_servers(remote_branches, remote_heads)
        self.annotated_tags = build_git_annotated_tags(self.path, annotated_tags)
        self.tags = tags
        self.upstreams = upstreams
        return self
