import os
import subprocess
import re
import pygraphviz

def get_git_files():
    result = []
    for each_dir in os.listdir('../.git/objects/'):
        if each_dir != 'info' and each_dir != 'pack':
            for each_file in os.listdir('../.git/objects/' + each_dir + '/'):
                result.append(each_dir + each_file)
    return result

def get_git_file_type(sha1_file):
    bashCommand = 'git cat-file -t ' + sha1_file
    output, error = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    if output:
        output = output.decode('utf-8')
        return output.splitlines()[0]

def read_git_file(sha1_file):
    bashCommand = 'git cat-file -p ' + sha1_file
    output, error = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE).communicate()
    output = output.decode('utf-8')
    return output.splitlines()

def build_git_nodes():
    blobs = []
    trees = []
    commits = []
    for each_git_file in get_git_files():
        each_git_file = each_git_file[:7]   # FIXME this can be skipped until display
        git_file_type = get_git_file_type(each_git_file)
        if git_file_type == 'blob':
            blobs.append(each_git_file)
        if git_file_type == 'tree':
            trees.append(each_git_file)
        if git_file_type == 'commit':
            commits.append(each_git_file)
    return blobs, trees, commits

class GitGraph:

    def __init__(self):
        self.blobs, self.trees, self.commits = build_git_nodes()
        self.tree_dependencies = self.__build_git_tree_dependencies()
        self.commit_dependencies = self.__build_git_commit_dependencies()
        self.graph = self.__build_git_graph()
    
    def get_graph(self):
        return self.graph

    def __build_git_one_tree_dependencies(self, sha1_file_tree):
        dependencies = []
        for each_line in read_git_file(sha1_file_tree):
            pattern = 'tree (.+)\t(.+)'
            match = re.search(pattern, each_line)
            if match:
                dependencies.append((sha1_file_tree[:7], match.group(1)[:7], match.group(2)))
            pattern = 'blob (.+)\t(.+)'
            match = re.search(pattern, each_line)
            if match:
                dependencies.append((sha1_file_tree[:7], match.group(1)[:7], match.group(2)))
        return dependencies

    def __build_git_one_commit_dependencies(self, sha1_file_tree):
        dependencies = []
        for each_line in read_git_file(sha1_file_tree):
            pattern = 'tree (.+)'
            match = re.search(pattern, each_line)
            if match:
                dependencies.append((sha1_file_tree[:7], match.group(1)[:7]))
            pattern = 'parent (.+)'
            match = re.search(pattern, each_line)
            if match:
                dependencies.append((sha1_file_tree[:7], match.group(1)[:7]))
        return dependencies

    def __build_git_tree_dependencies(self):
        dependencies = []
        for each_tree in self.trees:
            dependencies += self.__build_git_one_tree_dependencies(each_tree)
        return dependencies
    #    or
    #    dependencies= set()
    #    for each_tree in self.trees:
    #        dependencies.update(__build_git_one_tree_dependencies(each_tree))
    #    return dependencies

    def __build_git_commit_dependencies(self):
        dependencies = []
        for each_commit in self.commits:
            dependencies += self.__build_git_one_commit_dependencies(each_commit)
        return dependencies

    def __build_git_graph(self):
        graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
        graph += '\n\t// commits\n\tnode [fillcolor="#ffbb22"]\n'
        for each_commit in self.commits:
            graph += '\t"' + each_commit + '"\n'
        graph += '\n\t// trees\n\tnode [fillcolor="#ffccbb"]\n'
        for each_tree in self.trees:
            graph += '\t"' + each_tree + '"\n'
        graph += '\n\t// blobs\n\tnode [fillcolor="#ffdd33"]\n'
        for each_blob in self.blobs:
            graph += '\t"' + each_blob + '"\n'
        graph += '\n\t// dependencies\n'
        for each_dependency in self.commit_dependencies:
            graph += '\t"' + each_dependency[0] + '" -> "' + each_dependency[1] + '"\n'
        for each_dependency in self.tree_dependencies:
            graph += '\t"' + each_dependency[0] + '" -> "' + each_dependency[1] + '"\n'
        graph += '}\n'
        return graph





def build_git_graph_full():
    graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
    blobs, trees, commits = build_git_nodes()
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

