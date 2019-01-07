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
#     display_name: Python [conda env:jupy3]
#     language: python
#     name: conda-env-jupy3-py
# ---

# %load_ext autoreload
# %autoreload 2
# %autosave 0
import git_graph as gg
import git_functions as gf
import git_graph_display as gd

path = 'examples/allChords'

graph = gd.build_dot_graph(path, option='lhrdsu')
graph

graph = gd.build_dot_graph(path, option='lhrdsu')
gd.render(graph)
