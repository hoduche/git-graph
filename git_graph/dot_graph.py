import datetime

import graphviz

import git_graph.git_graph_class as gg

DEFAULT_FORMAT = 'pdf'
CURRENT_FOLDER = '.'
SHORT = 7

ALL = 'all'
COMMITS = 'commits'
BRANCHES = 'branches'

ALL_NODES = 'dchatsglurb'
COMMIT_NODES = ALL_NODES.replace('b', '').replace('t', '')
BRANCH_NODES = COMMIT_NODES.replace('c', '')


def get_git_repository(path):
    if (path / '.git').is_dir():
        return path
    else:
        parents = path.resolve().parents
        for each in parents:
            if (each / '.git').is_dir():
                return each


def handle_specific_node_sets(nodes=ALL_NODES):
    if nodes == ALL:
        result = ALL_NODES
    elif nodes == COMMITS:
        result = COMMIT_NODES
    elif nodes == BRANCHES:
        result = BRANCH_NODES
    else:
        result = nodes
    return result


def filter_nodes(git_graph, nodes=ALL_NODES):
    node_set = set()
    if 'b' in nodes:
        node_set.update(git_graph.blobs)
    if 't' in nodes:
        node_set.update(git_graph.trees)
    if 'c' in nodes:
        node_set.update(git_graph.commits)
    if 'l' in nodes:
        node_set.update(git_graph.local_branches)
    if 'h' in nodes:
        node_set.update(git_graph.local_head[0])
    if 'r' in nodes:
        node_set.update(git_graph.remote_branches)
    if 'd' in nodes:
        node_set.update(git_graph.remote_heads)
    if 's' in nodes:
        node_set.update(git_graph.remote_servers)
    if 'a' in nodes:
        node_set.update(git_graph.annotated_tags)
    if 'g' in nodes:
        node_set.update(git_graph.tags)
    if 'u' in nodes:
        pass
    return node_set


class DotGraph(graphviz.Digraph):

    def __init__(self, git_path, nodes=ALL_NODES):
        graphviz.Digraph.__init__(self, name='auto',
                                  graph_attr={'bgcolor': 'transparent'},
                                  node_attr={'style': 'filled',
                                             'fixedsize': 'true',
                                             'width': '0.95'})
        self.git_path = git_path
        git_graph = gg.GitGraph(self.git_path).build_graph()
        nodes = handle_specific_node_sets(nodes)
        node_set = filter_nodes(git_graph, nodes)
        if 'b' in nodes:
            for b in git_graph.blobs:
                self.node(b, label=b[:SHORT], fillcolor="#9ccc66")  # green
        if 't' in nodes:
            for t in git_graph.trees:
                self.node(t, label=t[:SHORT], fillcolor="#bc9b8f")  # brown
                for e in git_graph.trees[t]:
                    if e[0] in node_set:
                        self.edge(t, e[0])
        if 'c' in nodes:
            for c in git_graph.commits:
                self.node(c, label=c[:SHORT], fillcolor="#85d5fa")  # blue
                for e in git_graph.commits[c]:
                    if e in node_set:
                        self.edge(c, e)
        if 'l' in nodes:
            for l in git_graph.local_branches:
                self.node(l, label=l[:SHORT], fillcolor="#9999ff")  # violet
                e = git_graph.local_branches[l]
                if e in node_set:
                    self.edge(l, e)
        if 'h' in nodes:
            h = git_graph.local_head[0]
            self.node(h, label=h[:SHORT], fillcolor="#e6ccff")  # pale violet
            e = git_graph.local_head[1]
            if e in node_set:
                self.edge(h, e)
        if 'r' in nodes:
            for r in git_graph.remote_branches:
                self.node(r, label=r[r.find('/') + 1:][:SHORT],
                          fillcolor="#ffa366")  # orange
                e = git_graph.remote_branches[r]
                if e in node_set:
                    self.edge(r, e)
        if 'd' in nodes:
            for d in git_graph.remote_heads:
                self.node(d, label=d[d.find('/') + 1:][:SHORT],
                          fillcolor="#ffbeb3")  # pale orange
                e = git_graph.remote_heads[d]
                if e in node_set:
                    self.edge(d, e)
        if 's' in nodes:
            for s in git_graph.remote_servers:
                self.node(s, label=s[:SHORT], fillcolor="#ff6666")  # red
                for e in git_graph.remote_servers[s]:
                    if e in node_set:
                        self.edge(s, e)
        if 'a' in nodes:
            for a in git_graph.annotated_tags:
                self.node(a, label=a[:SHORT],
                          fillcolor="#ffdf80")  # pale yellow
                e = git_graph.annotated_tags[a]
                if e in node_set:
                    self.edge(a, e)
        if 'g' in nodes:
            for g in git_graph.tags:
                self.node(g, label=g[:SHORT], fillcolor="#ffc61a")  # yellow
                e = git_graph.tags[g]
                if e in node_set:
                    self.edge(g, e)
        if 'u' in nodes:  # no color (only edges)
            for u in git_graph.upstreams:
                e = git_graph.upstreams[u]
                if e in node_set:
                    self.edge(u, e)

    def persist(self, form=DEFAULT_FORMAT, conceal=True):
        self.format = form
        git_graph_path = self.git_path / '.gitGraph'
        if not git_graph_path.is_dir():
            git_graph_path.mkdir()
        dot_file_name = datetime.datetime.now().strftime(
            '%Y_%m_%d_%H_%M_%S_git_graph.dot')
        dot_file = git_graph_path / dot_file_name
        if conceal:
            self.render(dot_file)
        else:
            self.view(dot_file)
        image_file_name = dot_file_name + '.' + self.format
        return image_file_name
