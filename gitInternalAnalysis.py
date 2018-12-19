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

path = 'examples/git1'

for each_git_file in gg.get_git_files(path):
    print(each_git_file)

print(gg.get_git_file_type(path, '73eab88'))

for each_line in gg.read_git_file(path, '73eab88'):
    print(each_line)

blobs, trees, commits = gg.build_git_nodes(path)
print('blobs: ' + str(blobs))
print('trees: ' + str(trees))
print('commits: ' + str(commits))

Image(gg.display_git_graph(gg.GitGraph(path).build_graph()))



import graphviz
ps = graphviz.Digraph(name='pet-shop', node_attr={'shape': 'plaintext'})
#ps.node('parrot')
#ps.node('dead')
ps.edge('norwegian', 'blue')
ps

ps.view()

print(ps)
