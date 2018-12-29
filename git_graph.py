import collections
import os
import subprocess
import re

#import graphviz
import pathlib

import git_functions as gf


def get_git_remote_branches(path):
#    result = collections.defaultdict(list)
    for each_folder in os.listdir(path + '/.git/refs/remotes/'):
        for each_file in os.listdir(path + '/.git/refs/remotes/' + each_folder + '/'):
            with open(path + '/.git/refs/remotes/' + each_folder + '/' + each_file, 'r') as each_file_content:
                if each_file == 'HEAD':
                    line = each_file_content.readline()
                    info = line[line.rfind('/') + 1:-1]
                    print(each_folder + '/' + each_file + ' -> ' + info)
                else:
                    print(each_folder + '/' + each_file + ' -> ' + each_file_content.readline()[:7])
                #result[each_file].append(each_file_content.readline()[:7])
#    return result


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
#        self.remote_servers = 
#        self.remote_branches = get_git_remote_branches(self.path)
#        self.remote_heads = 
        self.annotated_tags = get_git_annotated_tags(self.path, annotated_tags)
        self.tags = get_git_tags(self.path)
        return self

    def filter_nodes(self, option=None):
        if not option:
            option = 'hlactbr'
        node_set = set()
        if 'h' in option:
            node_set.update(self.local_head)
        if 'l' in option:
            node_set.update(self.local_branches)
        if 'a' in option:
            node_set.update(self.tags)
            node_set.update(self.annotated_tags)
        if 'c' in option:
            node_set.update(self.commits)
        if 't' in option:
            node_set.update(self.trees)
        if 'b' in option:
            node_set.update(self.blobs)
        return node_set

    def build_dot_graph(self, option=None):
        if not option:
            option = 'hlactbr'
        node_set = self.filter_nodes(option)
        graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
        if 'h' in option:
            for h in self.local_head:
                graph += '\t"' + h[:7] + '" [fillcolor="lightblue"]\n'
                for e in self.local_head[h]:
                    if e in node_set:
                        graph += '\t"' + h[:7] + '" -> "' + e[:7] + '"\n'
        if 'r' in option:
            for r in self.remote_branches:
                graph += '\t"' + r[:7] + '" [fillcolor="cyan"]\n'
                for e in self.remote_branches[r]:
                    if e in node_set:
                        graph += '\t"' + r[:7] + '" -> "' + e[:7] + '"\n'
        if 'l' in option:
            for l in self.local_branches:
                graph += '\t"' + l[:7] + '" [fillcolor="green"]\n'
                for e in self.local_branches[l]:
                    if e in node_set:
                        graph += '\t"' + l[:7] + '" -> "' + e[:7] + '"\n'
        if 'a' in option:
            for a in self.tags:
                graph += '\t"' + a[:7] + '" [fillcolor="#ff0022"]\n'
                for e in self.tags[a]:
                    if e in node_set:
                        graph += '\t"' + a[:7] + '" -> "' + e[:7] + '"\n'
        if 'a' in option:
            for a in self.annotated_tags:
                graph += '\t"' + a[:7] + '" [fillcolor="#ff6622"]\n'
                for e in self.annotated_tags[a]:
                    if e in node_set:
                        graph += '\t"' + a[:7] + '" -> "' + e[:7] + '"\n'
        if 'c' in option:
            for c in self.commits:
                graph += '\t"' + c[:7] + '" [fillcolor="#ffbb22"]\n'
                for e in self.commits[c]:
                    if e in node_set:
                        graph += '\t"' + c[:7] + '" -> "' + e[:7] + '"\n'
        if 't' in option:
            for t in self.trees:
                graph += '\t"' + t[:7] + '" [fillcolor="#ffccbb"]\n'
                for e in self.trees[t]:
                    if e[0] in node_set:
                        graph += '\t"' + t[:7] + '" -> "' + e[0][:7] + '"\n'
        if 'b' in option:
            for b in self.blobs:
                graph += '\t"' + b[:7] + '" [fillcolor="#ffdd33"]\n'
        graph += '}\n'
        return graph

    def build_dot_graph_bu(self, option=None):
        if not option:
            option = 'hlactbr'
        graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
        if 'h' in option:
            for h in self.local_head:
                graph += '\t"' + h + '" [fillcolor="lightblue"]\n'
                if 'b' in option:
                    graph += '\t"' + h + '" -> {"' + '", "'.join(e for e in self.local_head[h]) + '"}\n'
        if 'l' in option:
            for l in self.local_branches:
                graph += '\t"' + l + '" [fillcolor="green"]\n'
                if 'c' in option:
                    graph += '\t"' + l + '" -> {"' + '", "'.join(e for e in self.local_branches[l]) + '"}\n'
        if 'a' in option:
            for a in self.tags:
                graph += '\t"' + a + '" [fillcolor="#ff0022"]\n'
                # annotated_tag or commit
                graph += '\t"' + a + '" -> {"' + '", "'.join(e for e in self.tags[a]) + '"}\n'
        if 'a' in option:
            for a in self.annotated_tags:
                graph += '\t"' + a + '" [fillcolor="#ff6622"]\n'
                if 'c' in option:
                    graph += '\t"' + a + '" -> {"' + '", "'.join(e for e in self.annotated_tags[a]) + '"}\n'
        if 'c' in option:
            for c in self.commits:
                graph += '\t"' + c + '" [fillcolor="#ffbb22"]\n'
                # tree or commit
                graph += '\t"' + c + '" -> {"' + '", "'.join(e for e in self.commits[c]) + '"}\n'
        if 't' in option:
            for t in self.trees:
                graph += '\t"' + t + '" [fillcolor="#ffccbb"]\n'
                # tree or blob
                graph += '\t"' + t + '" -> {"' + '", "'.join(e[0] for e in self.trees[t]) + '"}\n'
        if 'b' in option:
            for b in self.blobs:
                graph += '\t"' + b + '" [fillcolor="#ffdd33"]\n'
        graph += '}\n'
        return graph

    def display(self, option=None):
        with open('auto.dot', 'w+') as digraph_file:
            digraph_file.write(self.build_dot_graph(option))
        bashCommand = 'dot -Tpng auto.dot -o auto.png'
        subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
        return 'auto.png'


def build_git_graph_full():
    graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
    blobs, trees, commits, annotated_tags = get_git_objects()
    graph += '\n\t// commits\n\tnode [fillcolor="#ffbb22"]\n'
    for each_commit in commits:
        graph += '\t"' + each_commit + '" [label = <C_0: <font point-size="9">"' + each_commit + '"</font>>]\n'
    graph += '\n\t// trees\n\tnode [fillcolor="#ffccbb"]\n'
    for each_tree in trees:
        graph += '\t"' + each_tree + '" [label = <T_0: <font point-size="9">"' + each_tree + '"</font>>]\n'
    graph += '\n\t// blobs\n\tnode [fillcolor="#ffdd33"]\n'
    for each_blob in blobs:
        graph += '\t"' + each_blob + '" [label = <B_0: <font point-size="9">"' + each_blob + '"</font>>]\n'
    graph += '\n\t// dependencies\n'
    for each_commit in commits:
        for each_dependency in build_git_one_commit_dependencies(each_commit):
            graph += '\t"' + each_dependency[0] + '" -> "' + each_dependency[1] + '"\n'
    for each_tree in trees:
        for each_dependency in build_git_one_tree_dependencies(each_tree):
            graph += '\t"' + each_dependency[0] + '" -> "' + each_dependency[1] + '" [label="' + each_dependency[2] + '"]\n'
    graph += '}\n'
    return graph

