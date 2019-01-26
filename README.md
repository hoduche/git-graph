# View your Git repository as a Directed Acyclic Graph (DAG)
Git is by far the most popular version control system. 

However learning or teaching Git can seem daunting because of its impressive number of commands.

As Git is very lightweight, a good practice to better grasp the impact of a git command is to quickly setup a test project 
and experiment the effects of the command on it.

Git-graph is a git plugin written in Python that displays your git repository's inner content as a Directed Acyclic Graph (DAG).
This visual representation of git internal data before and after each command considerably improves the learning curve.   

# install git-graph
pip install git-graph

# run git-graph
git graph
git graph -p examples/demo -n btc -f svg

# run python module in interpreter
cd git_graph
python
>>> import dot_graph as dg
>>> dg.DotGraph('..').persist(conceal=True)
>>> dg.DotGraph('../examples/demo', nodes='btc').persist(form='svg', conceal=True)

# run python program
python git_graph/dot_graph.py
python git_graph/dot_graph.py -p examples/demo -n btc -f svg

# run python program with shebang
./git_graph/dot_graph.py
./git_graph/dot_graph.py -p examples/demo -n btc -f svg
