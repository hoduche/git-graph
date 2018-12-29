# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: jupy3
#     language: python
#     name: jupy3
# ---

# %load_ext autoreload
# %autoreload 2
# %autosave 0
from IPython.display import Image
import git_graph as gg
import git_functions as gf
import git_graph_display as gd

path = 'examples/branch'

Image(gd.display(gg.GitGraph(path).build_graph()))

gg.get_git_local_branches(path)

gg.get_git_local_head(path)

gg.get_git_tags(path)

gf.read_git_file(path, 'aee3d18')

gf.get_git_file_type(path, 'aee3d18')

gg.get_git_annotated_tags(path, annotated_tags)

gg.get_git_trees(path, trees)

gg.get_git_commits(path, commits)

Image(gg.GitGraph('.').build_graph().display())

Image(gg.GitGraph(path).build_graph().display())

import graphviz
ps = graphviz.Digraph(name='pet-shop', node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
ps.node('1234567', fillcolor="green")
ps.node('9999999', fillcolor="#ffbb22")
ps.node('norwayg', fillcolor="#ff0022")
ps.node('v2', fillcolor="#ff6622")
ps.edge('norwayg', '9999999')
ps.edge('norwayg', '1234567')
ps.edge('1234567', 'v2')
ps

ps.view()

print(ps)
