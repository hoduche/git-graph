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
import git_graph as gg
import git_functions as gf
import dot_graph as dg

path = 'examples/branch'

dg.DotGraph(path, option='bt')

dg.DotGraph(path).persist()

dg.DotGraph(path).persist(form='svg', show=False)
