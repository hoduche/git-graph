import subprocess

#import graphviz

import git_graph as gg


def filter_nodes(git_graph, option=None):
    if not option:
        option = 'hlactbr'
    node_set = set()
    if 'h' in option:
        node_set.update(git_graph.local_head)
    if 'l' in option:
        node_set.update(git_graph.local_branches)
    if 'a' in option:
        node_set.update(git_graph.tags)
        node_set.update(git_graph.annotated_tags)
    if 'c' in option:
        node_set.update(git_graph.commits)
    if 't' in option:
        node_set.update(git_graph.trees)
    if 'b' in option:
        node_set.update(git_graph.blobs)
    return node_set


def build_dot_graph(git_graph, option=None):
    if not option:
        option = 'hlactbr'
    node_set = filter_nodes(git_graph, option)
    graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
    if 'h' in option:
        for h in git_graph.local_head:
            graph += '\t"' + h[:7] + '" [fillcolor="lightblue"]\n'
            for e in git_graph.local_head[h]:
                if e in node_set:
                    graph += '\t"' + h[:7] + '" -> "' + e[:7] + '"\n'
    if 'r' in option:
        for r in git_graph.remote_branches:
            graph += '\t"' + r[:7] + '" [fillcolor="cyan"]\n'
            for e in git_graph.remote_branches[r]:
                if e in node_set:
                    graph += '\t"' + r[:7] + '" -> "' + e[:7] + '"\n'
    if 'l' in option:
        for l in git_graph.local_branches:
            graph += '\t"' + l[:7] + '" [fillcolor="green"]\n'
            for e in git_graph.local_branches[l]:
                if e in node_set:
                    graph += '\t"' + l[:7] + '" -> "' + e[:7] + '"\n'
    if 'a' in option:
        for a in git_graph.tags:
            graph += '\t"' + a[:7] + '" [fillcolor="#ff0022"]\n'
            for e in git_graph.tags[a]:
                if e in node_set:
                    graph += '\t"' + a[:7] + '" -> "' + e[:7] + '"\n'
    if 'a' in option:
        for a in git_graph.annotated_tags:
            graph += '\t"' + a[:7] + '" [fillcolor="#ff6622"]\n'
            for e in git_graph.annotated_tags[a]:
                if e in node_set:
                    graph += '\t"' + a[:7] + '" -> "' + e[:7] + '"\n'
    if 'c' in option:
        for c in git_graph.commits:
            graph += '\t"' + c[:7] + '" [fillcolor="#ffbb22"]\n'
            for e in git_graph.commits[c]:
                if e in node_set:
                    graph += '\t"' + c[:7] + '" -> "' + e[:7] + '"\n'
    if 't' in option:
        for t in git_graph.trees:
            graph += '\t"' + t[:7] + '" [fillcolor="#ffccbb"]\n'
            for e in git_graph.trees[t]:
                if e[0] in node_set:
                    graph += '\t"' + t[:7] + '" -> "' + e[0][:7] + '"\n'
    if 'b' in option:
        for b in git_graph.blobs:
            graph += '\t"' + b[:7] + '" [fillcolor="#ffdd33"]\n'
    graph += '}\n'
    return graph


def build_dot_graph_bu(git_graph, option=None):
    if not option:
        option = 'hlactbr'
    graph = 'digraph g{\n\tbgcolor="transparent"\n\tnode [style=filled]\n'
    if 'h' in option:
        for h in git_graph.local_head:
            graph += '\t"' + h + '" [fillcolor="lightblue"]\n'
            if 'b' in option:
                graph += '\t"' + h + '" -> {"' + '", "'.join(e for e in git_graph.local_head[h]) + '"}\n'
    if 'l' in option:
        for l in git_graph.local_branches:
            graph += '\t"' + l + '" [fillcolor="green"]\n'
            if 'c' in option:
                graph += '\t"' + l + '" -> {"' + '", "'.join(e for e in git_graph.local_branches[l]) + '"}\n'
    if 'a' in option:
        for a in git_graph.tags:
            graph += '\t"' + a + '" [fillcolor="#ff0022"]\n'
            # annotated_tag or commit
            graph += '\t"' + a + '" -> {"' + '", "'.join(e for e in git_graph.tags[a]) + '"}\n'
    if 'a' in option:
        for a in git_graph.annotated_tags:
            graph += '\t"' + a + '" [fillcolor="#ff6622"]\n'
            if 'c' in option:
                graph += '\t"' + a + '" -> {"' + '", "'.join(e for e in git_graph.annotated_tags[a]) + '"}\n'
    if 'c' in option:
        for c in git_graph.commits:
            graph += '\t"' + c + '" [fillcolor="#ffbb22"]\n'
            # tree or commit
            graph += '\t"' + c + '" -> {"' + '", "'.join(e for e in git_graph.commits[c]) + '"}\n'
    if 't' in option:
        for t in git_graph.trees:
            graph += '\t"' + t + '" [fillcolor="#ffccbb"]\n'
            # tree or blob
            graph += '\t"' + t + '" -> {"' + '", "'.join(e[0] for e in git_graph.trees[t]) + '"}\n'
    if 'b' in option:
        for b in git_graph.blobs:
            graph += '\t"' + b + '" [fillcolor="#ffdd33"]\n'
    graph += '}\n'
    return graph


def display(git_graph, option=None):
    with open('auto.dot', 'w+') as digraph_file:
        digraph_file.write(build_dot_graph(git_graph, option))
    bash_command = 'dot -Tpng auto.dot -o auto.png'
    subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE).communicate()
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

