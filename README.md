# Learn Git in one hour by viewing the inner of your Git repository as a graph
Git is by far the most popular version control system. 

However learning or teaching Git can seem daunting because of its impressive number of commands.

As Git is very lightweight, a good practice to better grasp the impact of a git command is to experiment its effects on a freshly setup test project.

Git-graph is a git plugin written in Python that displays your git repository's inner content as a Directed Acyclic Graph (DAG).
This visual representation of git internal data before and after each command considerably improves the learning curve.   

# What it does
Running git graph on a Git repository will:
1. scan you .git folder
2. build and save a graph representation as text (.dot) and image (pdf by default) in a .gitGraph folder
3. popup a window that displays the image of your graph

There is a color code to help distinguishing in the graph the different objects Git is using in its implementation:
* blobs are represented in green: "#9ccc66"
* trees are represented in brown: "#bc9b8f"
* commits are represented in blue: "#85d5fa"
* local branches are represented in violet: "#9999ff"
* local head is represented in pale violet: "#e6ccff"
* remote branches are represented in orange: "#ffa366"
* remote heads are represented in pale orange: "#ffbeb3"
* remote servers are represented in red: "#ff6666"
* annotated tags are represented in pale yellow: "#ffdf80"
* tags are represented in yellow: "#ffc61a"

By default all nodes are displayed in the output graph when running 'git graph'
To focus the display on what you are interested in monitoring,
it is possible to select only certain types of objects in the graph with the -n option
for instance to only display blob, trees and commits:
git graph -n btc

The default output format is pdf.
Other output graphics format (either vector or raster) can be set with the -f (or --format) option
for instance:
git graph -f svg
the full list of possible formats can be found on the Graphviz documentation website:
https://graphviz.gitlab.io/_pages/doc/info/output.html

By default git graph considers it is launched from a Git repository (ie where a .git folder can be found).
It is possible to indicate the path of another Git repository with the -p (or --path) option
git graph -p examples/demo

Finally it is possible to prevent the graph image popup with the -c (or --conceal) option
git graph -c

# Installation

Git-graph can be installed from GitHub, PiPY (the Python package index) or Conda.

### From GitHub
For developers, installing Git-graph from GitHub is probably the best option.

You first need to install the Graphviz software
(from a package manager or by downloading its installer at:
https://www.graphviz.org/download/)
and check that the dot binary is correctly set in you system's path

Then you you can clone this GitHub repository:
git clone https://github.com/hoduche/git-graph

Finally you will have to run the setup.py file:
python setup.py install

### From PyPI
git-graph package can be found on PyPI at:
https://pypi.org/project/git-graph/

To install it, you first need to install Graphviz from a package manager or by downloading its installer at:
https://www.graphviz.org/download/

Then you can run: 
pip install git-graph

### From Conda
If you are interested by the power of Conda, this might be the simple option to install git-graph.
With Conda, it is not required to install Graphviz separately as it is declared as a dependency to git-graph
and Conda knows how to install it.
You just have to run:
conda install git-graph

# Run
Git-graph should preferably be run as a Git plugin with the command git graph

It can also be run as a Python program or module

### Run as a Git plugin
git graph
git graph -p examples/demo -n btc -f svg

### Run python program
python git_graph/dot_graph.py
python git_graph/dot_graph.py -p examples/demo -n btc -f svg

### Run python program with shebang
./git_graph/dot_graph.py
./git_graph/dot_graph.py -p examples/demo -n btc -f svg

### Run python module in interpreter
cd git_graph
python
>>> import dot_graph as dg
>>> dg.DotGraph('..').persist(conceal=True)
>>> dg.DotGraph('../examples/demo', nodes='btc').persist(form='svg', conceal=True)
