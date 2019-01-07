import tempfile

import graphviz

import git_graph as gg

full_option = 'dchatsglurb'


def render(dot_graph, multiple=True):
    if multiple:
        temp_file = tempfile.mkstemp(prefix='auto.', suffix='.dot', dir='.')
        dot_graph.view(temp_file[1])
    else:
        dot_graph.render('auto.dot', view=False)


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
        node_set.update(git_graph.local_head[0])
    if 'r' in option:
        node_set.update(git_graph.remote_branches)
    if 'd' in option:
        node_set.update(git_graph.remote_heads)
    if 's' in option:
        node_set.update(git_graph.remote_servers)
    if 'a' in option:
        node_set.update(git_graph.annotated_tags)
    if 'g' in option:
        node_set.update(git_graph.tags)
    if 'u' in option:
        pass
    return node_set


def build_dot_graph(path, option=None, form='png'):
    if not option:
        option = full_option
    git_graph = gg.GitGraph(path).build_graph()
    node_set = filter_nodes(git_graph, option)
    dot_graph = graphviz.Digraph(name='auto', format=form,
                             graph_attr={'bgcolor': 'transparent'},
                             node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
    if 'b' in option:
        for b in git_graph.blobs:
            dot_graph.node(b, label=b[:7], fillcolor="#9ccc66")  # green
    if 't' in option:
        for t in git_graph.trees:
            dot_graph.node(t, label=t[:7], fillcolor="#bc9b8f")  # brown
            for e in git_graph.trees[t]:
                if e[0] in node_set:
                    dot_graph.edge(t, e[0])
    if 'c' in option:
        for c in git_graph.commits:
            dot_graph.node(c, label=c[:7], fillcolor="#6cccf9")  # blue
            for e in git_graph.commits[c]:
                if e in node_set:
                    dot_graph.edge(c, e)
    if 'l' in option:
        for l in git_graph.local_branches:
            dot_graph.node(l, label=l[:7], fillcolor="#ffc61a")  # yellow
            e = git_graph.local_branches[l]
            if e in node_set:
                dot_graph.edge(l, e)
    if 'h' in option:
        h = git_graph.local_head[0]
        dot_graph.node(h, label=h[:7], fillcolor="#cc99ff")  # violet
        e = git_graph.local_head[1]
        if e in node_set:
            dot_graph.edge(h, e)
    if 'r' in option:
        for r in git_graph.remote_branches:
            dot_graph.node(r, label=r[r.find('/') + 1:][:7], fillcolor="#ff6666")  # red
            e = git_graph.remote_branches[r]
            if e in node_set:
                dot_graph.edge(r, e)
    if 'd' in option:
        for d in git_graph.remote_heads:
            dot_graph.node(d, label=d[d.find('/') + 1:][:7], fillcolor="#ffa366")  # orange
            e = git_graph.remote_heads[d]
            if e in node_set:
                dot_graph.edge(d, e)
    if 's' in option:
        for s in git_graph.remote_servers:
            dot_graph.node(s, label=s[:7], fillcolor="#ff9988")  # salmon
            for e in git_graph.remote_servers[s]:
                if e in node_set:
                    dot_graph.edge(s, e)
    if 'a' in option:
        for a in git_graph.annotated_tags:
            dot_graph.node(a, label=a[:7], fillcolor="#00cc99")  # turquoise
            e = git_graph.annotated_tags[a]
            if e in node_set:
                dot_graph.edge(a, e)
    if 'g' in option:
        for g in git_graph.tags:
            dot_graph.node(g, label=g[:7], fillcolor="#ff66b3")  # pink
            e = git_graph.tags[g]
            if e in node_set:
                dot_graph.edge(g, e)
    if 'u' in option:  # no color (only edges)
        for u in git_graph.upstreams:
            e = git_graph.upstreams[u]
            if e in node_set:
                dot_graph.edge(u, e)
    return dot_graph
