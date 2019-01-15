#!/usr/bin/env python3

import argparse
import tempfile

import graphviz
import pathlib

import git_graph as gg

all_nodes = 'dchatsglurb'
default_format = 'pdf'
current_folder = '.'
short = 7


def filter_nodes(git_graph, nodes=all_nodes):
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

    def __init__(self, path, nodes=all_nodes):
        graphviz.Digraph.__init__(self, name='auto',
                                  graph_attr={'bgcolor': 'transparent'},
                                  node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
        self.path = path
        git_graph = gg.GitGraph(self.path).build_graph()
        node_set = filter_nodes(git_graph, nodes)
        if 'b' in nodes:
            for b in git_graph.blobs:
                self.node(b, label=b[:short], fillcolor="#9ccc66")  # green
        if 't' in nodes:
            for t in git_graph.trees:
                self.node(t, label=t[:short], fillcolor="#bc9b8f")  # brown
                for e in git_graph.trees[t]:
                    if e[0] in node_set:
                        self.edge(t, e[0])
        if 'c' in nodes:
            for c in git_graph.commits:
                self.node(c, label=c[:short], fillcolor="#85d5fa")  # blue
                for e in git_graph.commits[c]:
                    if e in node_set:
                        self.edge(c, e)
        if 'l' in nodes:
            for l in git_graph.local_branches:
                self.node(l, label=l[:short], fillcolor="#9999ff")  # violet
                e = git_graph.local_branches[l]
                if e in node_set:
                    self.edge(l, e)
        if 'h' in nodes:
            h = git_graph.local_head[0]
            self.node(h, label=h[:short], fillcolor="#e6ccff")  # pale violet
            e = git_graph.local_head[1]
            if e in node_set:
                self.edge(h, e)
        if 'r' in nodes:
            for r in git_graph.remote_branches:
                self.node(r, label=r[r.find('/') + 1:][:short], fillcolor="#ffa366")  # orange
                e = git_graph.remote_branches[r]
                if e in node_set:
                    self.edge(r, e)
        if 'd' in nodes:
            for d in git_graph.remote_heads:
                self.node(d, label=d[d.find('/') + 1:][:short], fillcolor="#ffbeb3")  # pale orange
                e = git_graph.remote_heads[d]
                if e in node_set:
                    self.edge(d, e)
        if 's' in nodes:
            for s in git_graph.remote_servers:
                self.node(s, label=s[:short], fillcolor="#ff6666")  # red
                for e in git_graph.remote_servers[s]:
                    if e in node_set:
                        self.edge(s, e)
        if 'a' in nodes:
            for a in git_graph.annotated_tags:
                self.node(a, label=a[:short], fillcolor="#ffdf80")  # pale yellow
                e = git_graph.annotated_tags[a]
                if e in node_set:
                    self.edge(a, e)
        if 'g' in nodes:
            for g in git_graph.tags:
                self.node(g, label=g[:short], fillcolor="#ffc61a")  # yellow
                e = git_graph.tags[g]
                if e in node_set:
                    self.edge(g, e)
        if 'u' in nodes:  # no color (only edges)
            for u in git_graph.upstreams:
                e = git_graph.upstreams[u]
                if e in node_set:
                    self.edge(u, e)

    def persist(self, form=default_format, show=True):
        self.format = form
        path = self.path + '/.gitGraph/'
        if not pathlib.Path(path).is_dir():
            pathlib.Path(path).mkdir()
        file = tempfile.mkstemp(prefix='auto.', suffix='.dot', dir=path)[1]
        if show:
            self.view(file)
        else:
            self.render(file)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Save and show your git repository as a graph')
    arg_parser.add_argument('-p', '--path', type=str, default=current_folder, help='Path to your git repository')
    arg_parser.add_argument('-n', '--nodes', type=str, default=all_nodes, help='Node types to display')
    arg_parser.add_argument('-f', '--format', type=str, default=default_format, help='Format of graph output')
    args = arg_parser.parse_args()

    DotGraph(args.path, nodes=args.nodes).persist(form=args.format, show=False)
