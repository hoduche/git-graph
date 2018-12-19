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

path = 'examples/git_test'

for each_git_file in gg.get_git_files(path):
    print(each_git_file)

print(gg.get_git_file_type(path, '73eab88'))

for each_line in gg.read_git_file(path, '73eab88'):
    print(each_line)

blobs, trees, commits = gg.build_git_nodes(path)
print('blobs: ' + str(blobs))
print('trees: ' + str(trees))
print('commits: ' + str(commits))

graph = gg.GitGraph(path)
digraph = graph.get_graph()
print(digraph)
with open('auto.dot', 'w+') as digraph_file:
    digraph_file.write(digraph)



import graphviz
ps = graphviz.Digraph(name='pet-shop', node_attr={'shape': 'plaintext'})
#ps.node('parrot')
#ps.node('dead')
ps.edge('norwegian', 'blue')
ps

print(ps)
