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
from IPython.display import Image
import git_graph as gg

path = 'examples/branch'

gg.get_git_head(path)

gg.get_git_local_branches(path)

gg.get_git_tags(path)

for each_git_file in gg.get_git_object_files(path):
    print(each_git_file)

print(gg.get_git_file_type(path, '3d06bbd'))

gg.read_git_file(path, '3d06bbd')

gg.read_git_file(path, 'aee3d18')

blobs, trees, commits, annotated_tags = gg.get_git_objects(path)
print('blobs: ' + str(blobs))
print('trees: ' + str(trees))
print('commits: ' + str(commits))
print('annotated tags: ' + str(annotated_tags))

gg.get_git_annotated_tags(path, annotated_tags)

gg.get_git_trees(path, trees)

gg.get_git_commits(path, commits)

Image(gg.GitGraph(path).build_graph().display())

Image(gg.GitGraph(path).build_graph().display('hlc'))

graph = gg.GitGraph(path).build_graph()
graph.filter_nodes()

import graphviz
ps = graphviz.Digraph(name='pet-shop', node_attr={'shape': 'plaintext'})
#ps.node('parrot')
#ps.node('dead')
ps.edge('norwegian', 'blue')
ps

ps.view()

print(ps)
