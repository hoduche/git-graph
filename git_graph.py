import collections
import os
import subprocess
import re

#import graphviz
from IPython.display import Image


def display_git_graph(git_graph):
    with open('auto.dot', 'w+') as digraph_file:
        digraph_file.write(git_graph)
    bashCommand = 'dot -Tpng auto.dot -o auto.png'
    subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    return 'auto.png'

def get_git_object_files(path):
    result = []
    for each_dir in os.listdir(path + '/.git/objects/'):
        if each_dir != 'info' and each_dir != 'pack':
            for each_file in os.listdir(path + '/.git/objects/' + each_dir + '/'):
                result.append(each_dir + each_file)
    return result

def get_git_file_type(path, sha1_file):
    bashCommand = 'git -C ' + path + ' cat-file -t ' + sha1_file
    output, error = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    if output:
        output = output.decode('utf-8')
        return output.splitlines()[0]

def read_git_file(path, sha1_file):
    bashCommand = 'git -C ' + path + ' cat-file -p ' + sha1_file
    output, error = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    output = output.decode('utf-8')
    return output.splitlines()

def get_git_objects(path):
    blobs = []
    trees = []
    commits = []
    annotated_tags = []
    for each_git_file in get_git_object_files(path):
        each_git_file = each_git_file[:7]   # FIXME this can be skipped until display
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

def get_git_local_branches(path):
    return __parse_oneline_content_git_folder(path, 'refs/heads')

def get_git_tags(path):
    return __parse_oneline_content_git_folder(path, 'refs/tags')

def get_git_head(path):
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
        for each_line in read_git_file(path, each_tree):
            match = re.search(pattern, each_line)
            if match:
                result[each_tree].append((match.group(2)[:7], match.group(3)))
    return result

def get_git_commits(path, commits):
    result = collections.defaultdict(list)
    pattern = '(tree|parent) (.+)'
    for each_commit in commits:
        for each_line in read_git_file(path, each_commit):
            match = re.search(pattern, each_line)
            if match:
                result[each_commit].append(match.group(2)[:7])
    return result

def get_git_annotated_tags(path, annotated_tags):
    result = collections.defaultdict(list)
    pattern = '(object) (.+)'
    for each_annotated_tag in annotated_tags:
        for each_line in read_git_file(path, each_annotated_tag):
            match = re.search(pattern, each_line)
            if match:
                result[each_annotated_tag].append(match.group(2)[:7])
    return result

class GitGraph:

    def __init__(self, path):
        self.path = path
        self.head = collections.defaultdict(list)
        self.blobs = []
        self.trees = collections.defaultdict(list)
        self.commits = collections.defaultdict(list)
        self.annotated_tags = collections.defaultdict(list)
        self.tags = collections.defaultdict(list)
        self.local_branches = collections.defaultdict(list)
        self.remote_branches = collections.defaultdict(list)
        self.dot_graph = ''

    def build_graph(self):
        self.head = get_git_head(self.path)
        self.blobs, trees, commits, annotated_tags = get_git_objects(self.path)
        self.trees = get_git_trees(self.path, trees)
        self.commits = get_git_commits(self.path, commits)
        self.annotated_tags = get_git_annotated_tags(self.path, annotated_tags)
        self.tags = get_git_tags(self.path)
        self.local_branches = get_git_local_branches(self.path)
        return self

    def filter_nodes(self, option=None):
        if not option:
            option = 'hlactbr'
        node_set = set()
        if 'h' in option:
            node_set.update(self.head)
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
            for h in self.head:
                graph += '\t"' + h + '" [fillcolor="lightblue"]\n'
                for e in self.head[h]:
                    if e in node_set:
                        graph += '\t"' + h + '" -> "' + e + '"\n'
        if 'l' in option:
            for l in self.local_branches:
                graph += '\t"' + l + '" [fillcolor="green"]\n'
                for e in self.local_branches[l]:
                    if e in node_set:
                        graph += '\t"' + l + '" -> "' + e + '"\n'
        if 'a' in option:
            for a in self.tags:
                graph += '\t"' + a + '" [fillcolor="#ff0022"]\n'
                for e in self.tags[a]:
                    if e in node_set:
                        graph += '\t"' + a + '" -> "' + e + '"\n'
        if 'a' in option:
            for a in self.annotated_tags:
                graph += '\t"' + a + '" [fillcolor="#ff6622"]\n'
                for e in self.annotated_tags[a]:
                    if e in node_set:
                        graph += '\t"' + a + '" -> "' + e + '"\n'
        if 'c' in option:
            for c in self.commits:
                graph += '\t"' + c + '" [fillcolor="#ffbb22"]\n'
                for e in self.commits[c]:
                    if e in node_set:
                        graph += '\t"' + c + '" -> "' + e + '"\n'
        if 't' in option:
            for t in self.trees:
                graph += '\t"' + t + '" [fillcolor="#ffccbb"]\n'
                for e in self.trees[t]:
                    if e[0] in node_set:
                        graph += '\t"' + t + '" -> "' + e[0] + '"\n'
        if 'b' in option:
            for b in self.blobs:
                graph += '\t"' + b + '" [fillcolor="#ffdd33"]\n'
        graph += '}\n'
        return graph

    def build_dot_graph_bu(self, option=None):
        if not option:
            option = 'hlactbr'
        graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
        if 'h' in option:
            for h in self.head:
                graph += '\t"' + h + '" [fillcolor="lightblue"]\n'
                if 'b' in option:
                    graph += '\t"' + h + '" -> {"' + '", "'.join(e for e in self.head[h]) + '"}\n'
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




def __parse_oneline_content_git_folder(path, folder):
    result = collections.defaultdict(list)
    folder = path + '/.git/' + folder + '/'
    for each_file in os.listdir(folder):
        with open(folder + each_file, 'r') as each_file_content:
            result[each_file].append(each_file_content.readline()[:7])
    return result

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

