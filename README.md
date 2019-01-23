# View your Git repository as a Directed Acyclic Graph (DAG)
Git is by far the most popular version control system. 

However learning or teaching Git can seem daunting because of its impressive number of commands.

As Git is very lightweight, a good practice to better grasp the impact of a git command is to quickly setup a test project 
and experiment the effects of the command on it.

Git-graph is a git plugin written in Python that displays your git repository's inner content as a Directed Acyclic Graph (DAG).
This visual representation of git internal data before and after each command considerably improves the learning curve.   

# create conda environment
conda create -n git
source activate git (conda activate git on windows)
conda install --file requirements.txt

# run python module in interpreter
cd git-graph
python
>>> import dot_graph as dg
>>> dg.DotGraph('..').persist(show=False)
>>> dg.DotGraph('../examples/demo', nodes='btc').persist(form='svg', show=False)

# run python program
python git-graph/dot_graph.py
python git-graph/dot_graph.py -p examples/demo -n btc -f svg

# run python program with shebang
./git-graph/dot_graph.py
./git-graph/dot_graph.py -p examples/demo -n btc -f svg

# run python program with link in PATH
ln -s ~/workspace/git-graph/git-graph/dot_graph.py /home/hduche/conda/envs/git/bin/gg
cd examples/demo
gg
gg -p examples/demo -n btc -f svg

# run as git plugin
ln -s ~/workspace/git-graph/git-graph/dot_graph.py /home/hduche/conda/envs/git/bin/git-graph
git graph
git graph -p examples/demo -n btc -f svg
