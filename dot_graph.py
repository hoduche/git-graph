#!/usr/bin/env python3

import argparse
import tempfile

import graphviz
import pathlib

import git_graph as gg

full_option = 'dchatsglurb'
default_format = 'pdf'
short = 7


def filter_nodes(git_graph, option=full_option):
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


class DotGraph(graphviz.Digraph):

    def __init__(self, path, option=full_option):
        graphviz.Digraph.__init__(self, name='auto',
                                  graph_attr={'bgcolor': 'transparent'},
                                  node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
        self.path = path
        git_graph = gg.GitGraph(self.path).build_graph()
        node_set = filter_nodes(git_graph, option)
        if 'b' in option:
            for b in git_graph.blobs:
                self.node(b, label=b[:short], fillcolor="#9ccc66")  # green
        if 't' in option:
            for t in git_graph.trees:
                self.node(t, label=t[:short], fillcolor="#bc9b8f")  # brown
                for e in git_graph.trees[t]:
                    if e[0] in node_set:
                        self.edge(t, e[0])
        if 'c' in option:
            for c in git_graph.commits:
                self.node(c, label=c[:short], fillcolor="#85d5fa")  # blue
                for e in git_graph.commits[c]:
                    if e in node_set:
                        self.edge(c, e)
        if 'l' in option:
            for l in git_graph.local_branches:
                self.node(l, label=l[:short], fillcolor="#9999ff")  # violet
                e = git_graph.local_branches[l]
                if e in node_set:
                    self.edge(l, e)
        if 'h' in option:
            h = git_graph.local_head[0]
            self.node(h, label=h[:short], fillcolor="#e6ccff")  # pale violet
            e = git_graph.local_head[1]
            if e in node_set:
                self.edge(h, e)
        if 'r' in option:
            for r in git_graph.remote_branches:
                self.node(r, label=r[r.find('/') + 1:][:short], fillcolor="#ffa366")  # orange
                e = git_graph.remote_branches[r]
                if e in node_set:
                    self.edge(r, e)
        if 'd' in option:
            for d in git_graph.remote_heads:
                self.node(d, label=d[d.find('/') + 1:][:short], fillcolor="#ffbeb3")  # pale orange
                e = git_graph.remote_heads[d]
                if e in node_set:
                    self.edge(d, e)
        if 's' in option:
            for s in git_graph.remote_servers:
                self.node(s, label=s[:short], fillcolor="#ff6666")  # red
                for e in git_graph.remote_servers[s]:
                    if e in node_set:
                        self.edge(s, e)
        if 'a' in option:
            for a in git_graph.annotated_tags:
                self.node(a, label=a[:short], fillcolor="#ffdf80")  # pale yellow
                e = git_graph.annotated_tags[a]
                if e in node_set:
                    self.edge(a, e)
        if 'g' in option:
            for g in git_graph.tags:
                self.node(g, label=g[:short], fillcolor="#ffc61a")  # yellow
                e = git_graph.tags[g]
                if e in node_set:
                    self.edge(g, e)
        if 'u' in option:  # no color (only edges)
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
    arg_parser = argparse.ArgumentParser(description='Save and show your git repository')
    arg_parser.add_argument('-p', '--repo', type=str, default='.', help='Path to your git repository')
    arg_parser.add_argument('-o', '--option', type=str, default=full_option, help='Type of nodes to display')
    arg_parser.add_argument('-f', '--format', type=str, default=default_format, help='Graph output format')
#    arg_parser.add_argument('-s', '--show', action='store_false', help='popup graph output')
    args = arg_parser.parse_args()

    DotGraph(args.repo, option=args.option).persist(form=args.format, show=False)
