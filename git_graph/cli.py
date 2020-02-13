#!/usr/bin/env python

import argparse

import pathlib

from git_graph import __version__
import git_graph.dot_graph as dg


def main(args=None):
    example_text = '''examples:
    git graph
    git graph -p examples/demo -n btc -f svg
    '''

    node_text = '''node types to display in the graph (default is all).
    'commits' and 'branches' will focus output on commits and branches
    respectively.
    For further control, you can also pick the letters corresponding to
    your choice:
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

    parser = argparse.ArgumentParser(
        prog='git graph',
        description='Save and display your Git repositories inner content '
                    'as a Directed Acyclic Graph (DAG)',
        epilog=example_text,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-p', '--path', type=str, action='store', default='.',
                        help='path to your git repository (default is here)')
    parser.add_argument('-n', '--nodes', default=dg.ALL_NODES,
                        help=node_text)
    parser.add_argument('-f', '--format', default=dg.DEFAULT_FORMAT,
                        help='format of graph output: pdf, svg, png... '
                             '(default is pdf)')
    parser.add_argument('-c', '--conceal', action='store_true', default=False,
                        help='conceal graph (deactivated by default)')
    args = parser.parse_args(args=args)

    git_path = dg.get_git_repository(pathlib.Path(args.path))
    if git_path is not None:
        dot_graph = dg.DotGraph(git_path, nodes=args.nodes)
        file = dot_graph.persist(form=args.format, conceal=args.conceal)
        git_graph_path = git_path.resolve() / '.gitGraph'
        print(f'{file} saved in {git_graph_path}')
        return file
    else:
        print('Not a git repository')


# to debug real use cases, set in your Debug Configuration something like:
# Parameters = -n btc -f png
#
# this configuration is  generated automatically by pycharm at first debug
# it can be found in Run/Edit Configurations/Python
if __name__ == '__main__':
    main()
