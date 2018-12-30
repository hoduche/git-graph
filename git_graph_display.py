import tempfile

import graphviz

import git_graph as gg


full_option = 'chatblrsg'


def display_git_graph(path, option=None, temp=False):
    display(gg.GitGraph(path), option, temp)


def display(git_graph, option=None, temp=False):
    dot_graph = build_dot_graph(git_graph.build_graph(), option)
    if temp:
        dot_graph.view(tempfile.mktemp('auto.dot'))
    else:
        dot_graph.render('auto.dot', view=False)


def build_dot_graph(git_graph, option=None):
    if not option:
        option = full_option
    node_set = filter_nodes(git_graph, option)
    dot_graph = graphviz.Digraph(name='auto', format='png',
                             graph_attr={'bgcolor': 'transparent'},
                             node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
    if 'b' in option:
        for b in git_graph.blobs:
            dot_graph.node(b[:7], fillcolor="#9ccc66")
    if 't' in option:
        for t in git_graph.trees:
            dot_graph.node(t[:7], fillcolor="#bc9b8f")
            for e in git_graph.trees[t]:
                if e[0] in node_set:
                    dot_graph.edge(t[:7], e[0][:7])
    if 'c' in option:
        for c in git_graph.commits:
            dot_graph.node(c[:7], fillcolor="#6cccf9")
            for e in git_graph.commits[c]:
                if e in node_set:
                    dot_graph.edge(c[:7], e[:7])
    if 'l' in option:
        for l in git_graph.local_branches:
            dot_graph.node(l[:7], fillcolor="#ffc61a")
            for e in git_graph.local_branches[l]:
                if e in node_set:
                    dot_graph.edge(l[:7], e[:7])
    if 'h' in option:
        for h in git_graph.local_head:
            dot_graph.node(h[:7], fillcolor="#cc99ff")
            for e in git_graph.local_head[h]:
                if e in node_set:
                    dot_graph.edge(h[:7], e[:7])
    if 's' in option:
        for s in git_graph.remote_servers:
            dot_graph.node(s[:7], fillcolor="#ff9988")
            for e in git_graph.remote_servers[s]:
                if e in node_set:
                    dot_graph.edge(s[:7], e[:7])
    if 'r' in option:
        for r in git_graph.remote_branches:
            dot_graph.node(r[:7], fillcolor="#ff6666")
            for e in git_graph.remote_branches[r]:
                if e in node_set:
                    dot_graph.edge(r[:7], e[:7])
    if 'g' in option:
        for g in git_graph.tags:
            dot_graph.node(g[:7], fillcolor="#ff66b3")
            for e in git_graph.tags[g]:
                if e in node_set:
                    dot_graph.edge(g[:7], e[:7])
    if 'a' in option:
        for a in git_graph.annotated_tags:
            dot_graph.node(a[:7], fillcolor="#00cc99")
            for e in git_graph.annotated_tags[a]:
                if e in node_set:
                    dot_graph.edge(a[:7], e[:7])
    return dot_graph


def filter_nodes(git_graph, option=None):
    if not option:
        option = full_option
    node_set = set()
    if 'b' in option:
        node_set.update(git_graph.blobs)
    if 't' in option:
        node_set.update(git_graph.trees)
    if 'c' in option:
        node_set.update(git_graph.commits)
    if 'l' in option:
        node_set.update(git_graph.local_branches)
    if 'h' in option:
        node_set.update(git_graph.local_head)
    if 's' in option:
        node_set.update(git_graph.remote_servers)
    if 'r' in option:
        node_set.update(git_graph.remote_branches)
    if 'g' in option:
        node_set.update(git_graph.tags)
    if 'a' in option:
        node_set.update(git_graph.annotated_tags)
    return node_set
