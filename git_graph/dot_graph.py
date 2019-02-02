#!/usr/bin/env python

import argparse
import tempfile

import graphviz
import pathlib

import git_graph.git_graph as gg

ALL_NODES = 'dchatsglurb'
DEFAULT_FORMAT = 'pdf'
CURRENT_FOLDER = '.'
SHORT = 7


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

    def __init__(self, path, nodes=ALL_NODES):
        graphviz.Digraph.__init__(self, name='auto',
                                  graph_attr={'bgcolor': 'transparent'},
                                  node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
        self.path = path
        git_graph = gg.GitGraph(self.path).build_graph()
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
                self.node(r, label=r[r.find('/') + 1:][:SHORT], fillcolor="#ffa366")  # orange
                e = git_graph.remote_branches[r]
                if e in node_set:
                    self.edge(r, e)
        if 'd' in nodes:
            for d in git_graph.remote_heads:
                self.node(d, label=d[d.find('/') + 1:][:SHORT], fillcolor="#ffbeb3")  # pale orange
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
                self.node(a, label=a[:SHORT], fillcolor="#ffdf80")  # pale yellow
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
        path = self.path + '/.gitGraph/'
        if not pathlib.Path(path).is_dir():
            pathlib.Path(path).mkdir()
        file = tempfile.mkstemp(prefix='auto.', suffix='.dot', dir=path)[1]
        if conceal:
            self.render(file)
        else:
            self.view(file)


def main():
    example_text = '''examples:
    git graph
    git graph -p examples/demo -n btc -f svg
    '''

    node_text = '''node types to display in the graph: pick the letters corresponding to your choice (default is all)
    | Node type      | Letter |
    | -------------- | ------ |
    | blob           | b      |
    | tree           | t      |
    | commit         | c      |
    | local branche  | l      |
    | local head     | h      |
    | remote branche | r      |
    | remote head    | d      |
    | remote server  | s      |
    | annotated tag  | a      |
    | tag            | g      |
    | upstream link  | u      |
    '''

    arg_parser = argparse.ArgumentParser(prog='git graph',
                                         description='Save and display your Git repositories inner content '
                                                     'as a Directed Acyclic Graph (DAG)',
                                         epilog=example_text,
                                         formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('-p', '--path', type=str, action='store', default=CURRENT_FOLDER, help='path to your git repository (default is here)')
    arg_parser.add_argument('-n', '--nodes', type=str, action='store', default=ALL_NODES, help=node_text)
    arg_parser.add_argument('-f', '--format', type=str, action='store', default=DEFAULT_FORMAT, help='format of graph output: pdf, svg, png... (default is pdf)')
    arg_parser.add_argument('-c', '--conceal', dest='conceal', action='store_true', default=False, help='conceal graph (deactivated by default)')
    arg_parser.add_argument('-s', '--show', dest='conceal', action='store_false', default=False, help='show graph (activated by default)')
    args = arg_parser.parse_args()

    DotGraph(args.path, nodes=args.nodes).persist(form=args.format, conceal=args.conceal)


if __name__ == '__main__':
    main()
