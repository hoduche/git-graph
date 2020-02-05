import os
import subprocess

import git_graph.dot_graph as dg

author = "Bernard"
email = "author@cie.com"
action_date = "Sat Oct 15 11:00 2011 +0100"
os.environ["GIT_AUTHOR_NAME"] = author
os.environ["GIT_COMMITTER_NAME"] = author
os.environ["GIT_AUTHOR_EMAIL"] = email
os.environ["GIT_COMMITTER_EMAIL"] = email
os.environ["GIT_AUTHOR_DATE"] = action_date
os.environ["GIT_COMMITTER_DATE"] = action_date


def execute_bash_command(path, command):
    output, error = subprocess.Popen(command.split(), cwd=str(path), stdout=subprocess.PIPE).communicate()
    if not error:
        return output


def test_minimal_repo(tmp_path):
    dir1 = tmp_path / 'dir1'
    dir1.mkdir()
    file1 = dir1 / 'file1.txt'
    file1.write_text('content file1.txt v1')
    assert len(list(tmp_path.iterdir())) == 1
    assert file1.is_file()
    assert file1.read_text() == 'content file1.txt v1'

    file2 = tmp_path / 'file2.txt'
    file2.write_text('content file2.txt v1')
    assert len(list(tmp_path.iterdir())) == 2
    assert file2.is_file()
    assert file2.read_text() == 'content file2.txt v1'

    execute_bash_command(tmp_path, 'git init')
    assert len(list(tmp_path.iterdir())) == 3
    assert (tmp_path / '.git').is_dir()

    execute_bash_command(tmp_path, 'git add -A')
    execute_bash_command(tmp_path, 'git commit -m commit1')

    dg.DotGraph(tmp_path).persist()

    assert len(list(tmp_path.iterdir())) == 4
    assert (tmp_path / '.gitGraph').is_dir()
    assert len(list((tmp_path / '.gitGraph').iterdir())) == 2

    dot_file_path = list((tmp_path / '.gitGraph').glob('*.dot'))[0]
    with open(dot_file_path) as dot_file:
        dot_graph = dot_file.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        assert ''.join(dot_graph) == minimal_repo_dot_graph


minimal_repo_dot_graph = """digraph auto {
	graph [bgcolor=transparent]
	node [fixedsize=true style=filled width=0.95]
	"54378aec6a6ea34638ac687217745e574360285e" [label="54378ae" fillcolor="#9ccc66"]
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" -> "54378aec6a6ea34638ac687217745e574360285e"
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" [label="6e414aa" fillcolor="#bc9b8f"]
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> "6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92"
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8
	"737c972823aec2a30e726cd39821edf8d4b4826b" [label="737c972" fillcolor="#bc9b8f"]
	HEAD -> master
	HEAD [label=HEAD fillcolor="#e6ccff"]
	e53574e083bfb447086df95ad1214d87b6ae45c4 -> "737c972823aec2a30e726cd39821edf8d4b4826b"
	e53574e083bfb447086df95ad1214d87b6ae45c4 [label=e53574e fillcolor="#85d5fa"]
	ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8 [label=ecf7586 fillcolor="#9ccc66"]
	master -> e53574e083bfb447086df95ad1214d87b6ae45c4
	master [label=master fillcolor="#9999ff"]
}
"""


def test_full_repo(tmp_path):
    execute_bash_command(tmp_path, 'git init')

    dir1 = tmp_path / 'dir1'
    dir1.mkdir()
    file1 = dir1 / 'file1.txt'
    file1.write_text('content file1.txt v1')
    file2 = tmp_path / 'file2.txt'
    file2.write_text('content file2.txt v1')
    execute_bash_command(tmp_path, 'git add -A')
    execute_bash_command(tmp_path, 'git commit -m commit1')

    execute_bash_command(tmp_path, 'git branch idea1')
    execute_bash_command(tmp_path, 'git checkout idea1')

    file2.write_text('content file2.txt v2')
    file3 = tmp_path / 'file3.txt'
    file3.write_text('content file1.txt v1')
    execute_bash_command(tmp_path, 'git add -A')
    execute_bash_command(tmp_path, 'git commit -m commit2')

    execute_bash_command(tmp_path, 'git checkout master')
    execute_bash_command(tmp_path, 'git checkout -b idea2')
    file1.write_text('content file1.txt v2')
    execute_bash_command(tmp_path, 'git commit -am commit3')

    execute_bash_command(tmp_path, 'git checkout master')
    execute_bash_command(tmp_path, 'git merge idea2')
    execute_bash_command(tmp_path, 'git tag v0.0.1')

    execute_bash_command(tmp_path, 'git merge idea1 --no-edit')
#    execute_bash_command(tmp_path, 'git tag v0.0.2 -am "good job"')

    dg.DotGraph(tmp_path).persist()
    dot_file_path = list((tmp_path / '.gitGraph').glob('*.dot'))[0]
    with open(dot_file_path) as dot_file:
        dot_graph = dot_file.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        assert ''.join(dot_graph) == full_repo_dot_graph


full_repo_dot_graph = """digraph auto {
	graph [bgcolor=transparent]
	node [fixedsize=true style=filled width=0.95]
	"01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8" -> "8e26413dad1890d45502dd31a75f9c403eee2fef"
	"01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8" -> e53574e083bfb447086df95ad1214d87b6ae45c4
	"01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8" [label="01ccfc8" fillcolor="#85d5fa"]
	"0241c07298c9b2bb84793a02418716f302632564" -> "2358d7dee4b70234fb7078d735a835673dc4b45b"
	"0241c07298c9b2bb84793a02418716f302632564" -> "54378aec6a6ea34638ac687217745e574360285e"
	"0241c07298c9b2bb84793a02418716f302632564" -> f9f2794a3dae393bdb07affde1719aee32e6c236
	"0241c07298c9b2bb84793a02418716f302632564" [label="0241c07" fillcolor="#bc9b8f"]
	"0c213d3ee3c6dd438e02ea8f465548f8dd56288b" [label="0c213d3" fillcolor="#9ccc66"]
	"2358d7dee4b70234fb7078d735a835673dc4b45b" -> "0c213d3ee3c6dd438e02ea8f465548f8dd56288b"
	"2358d7dee4b70234fb7078d735a835673dc4b45b" [label="2358d7d" fillcolor="#bc9b8f"]
	"3447a63ea27b15856a751c3f631546ad6c98d07a" -> "01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8"
	"3447a63ea27b15856a751c3f631546ad6c98d07a" -> "0241c07298c9b2bb84793a02418716f302632564"
	"3447a63ea27b15856a751c3f631546ad6c98d07a" -> c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834
	"3447a63ea27b15856a751c3f631546ad6c98d07a" [label="3447a63" fillcolor="#85d5fa"]
	"54378aec6a6ea34638ac687217745e574360285e" [label="54378ae" fillcolor="#9ccc66"]
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" -> "54378aec6a6ea34638ac687217745e574360285e"
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" [label="6e414aa" fillcolor="#bc9b8f"]
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> "6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92"
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8
	"737c972823aec2a30e726cd39821edf8d4b4826b" [label="737c972" fillcolor="#bc9b8f"]
	"8e26413dad1890d45502dd31a75f9c403eee2fef" -> "54378aec6a6ea34638ac687217745e574360285e"
	"8e26413dad1890d45502dd31a75f9c403eee2fef" -> "6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92"
	"8e26413dad1890d45502dd31a75f9c403eee2fef" -> f9f2794a3dae393bdb07affde1719aee32e6c236
	"8e26413dad1890d45502dd31a75f9c403eee2fef" [label="8e26413" fillcolor="#bc9b8f"]
	"v0.0.1" -> c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834
	"v0.0.1" [label="v0.0.1" fillcolor="#ffc61a"]
	HEAD -> master
	HEAD [label=HEAD fillcolor="#e6ccff"]
	c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834 -> e04c9e73c27f423fecb1d8220c4a4b5ca217f2de
	c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834 -> e53574e083bfb447086df95ad1214d87b6ae45c4
	c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834 [label=c99b362 fillcolor="#85d5fa"]
	e04c9e73c27f423fecb1d8220c4a4b5ca217f2de -> "2358d7dee4b70234fb7078d735a835673dc4b45b"
	e04c9e73c27f423fecb1d8220c4a4b5ca217f2de -> ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8
	e04c9e73c27f423fecb1d8220c4a4b5ca217f2de [label=e04c9e7 fillcolor="#bc9b8f"]
	e53574e083bfb447086df95ad1214d87b6ae45c4 -> "737c972823aec2a30e726cd39821edf8d4b4826b"
	e53574e083bfb447086df95ad1214d87b6ae45c4 [label=e53574e fillcolor="#85d5fa"]
	ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8 [label=ecf7586 fillcolor="#9ccc66"]
	f9f2794a3dae393bdb07affde1719aee32e6c236 [label=f9f2794 fillcolor="#9ccc66"]
	idea1 -> "01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8"
	idea1 [label=idea1 fillcolor="#9999ff"]
	idea2 -> c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834
	idea2 [label=idea2 fillcolor="#9999ff"]
	master -> "3447a63ea27b15856a751c3f631546ad6c98d07a"
	master [label=master fillcolor="#9999ff"]
}
"""


def test_remote_repo(tmp_path):
    # resume from full_repo
    # git tag v0.0.2 -am "good job"
    # git remote add origin https://github.com/hoduche/git-empty.git
    # git push -u origin master
    # git checkout idea1
    # git push -u origin idea1
    # git checkout master
    # git push origin --tags

    execute_bash_command(tmp_path, 'git clone https://github.com/hoduche/git-empty .')
    execute_bash_command(tmp_path, 'git checkout -b idea1 origin/idea1')
    execute_bash_command(tmp_path, 'git branch idea2 v0.0.1')

    dg.DotGraph(tmp_path).persist()
    dot_file_path = list((tmp_path / '.gitGraph').glob('*.dot'))[0]
    with open(dot_file_path) as dot_file:
        dot_graph = dot_file.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        assert ''.join(dot_graph) == remote_repo_dot_graph


remote_repo_dot_graph = """digraph auto {
	graph [bgcolor=transparent]
	node [fixedsize=true style=filled width=0.95]
	"01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8" -> "8e26413dad1890d45502dd31a75f9c403eee2fef"
	"01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8" -> e53574e083bfb447086df95ad1214d87b6ae45c4
	"01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8" [label="01ccfc8" fillcolor="#85d5fa"]
	"0241c07298c9b2bb84793a02418716f302632564" -> "2358d7dee4b70234fb7078d735a835673dc4b45b"
	"0241c07298c9b2bb84793a02418716f302632564" -> "54378aec6a6ea34638ac687217745e574360285e"
	"0241c07298c9b2bb84793a02418716f302632564" -> f9f2794a3dae393bdb07affde1719aee32e6c236
	"0241c07298c9b2bb84793a02418716f302632564" [label="0241c07" fillcolor="#bc9b8f"]
	"0c213d3ee3c6dd438e02ea8f465548f8dd56288b" [label="0c213d3" fillcolor="#9ccc66"]
	"2358d7dee4b70234fb7078d735a835673dc4b45b" -> "0c213d3ee3c6dd438e02ea8f465548f8dd56288b"
	"2358d7dee4b70234fb7078d735a835673dc4b45b" [label="2358d7d" fillcolor="#bc9b8f"]
	"3447a63ea27b15856a751c3f631546ad6c98d07a" -> "01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8"
	"3447a63ea27b15856a751c3f631546ad6c98d07a" -> "0241c07298c9b2bb84793a02418716f302632564"
	"3447a63ea27b15856a751c3f631546ad6c98d07a" -> c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834
	"3447a63ea27b15856a751c3f631546ad6c98d07a" [label="3447a63" fillcolor="#85d5fa"]
	"54378aec6a6ea34638ac687217745e574360285e" [label="54378ae" fillcolor="#9ccc66"]
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" -> "54378aec6a6ea34638ac687217745e574360285e"
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" [label="6e414aa" fillcolor="#bc9b8f"]
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> "6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92"
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8
	"737c972823aec2a30e726cd39821edf8d4b4826b" [label="737c972" fillcolor="#bc9b8f"]
	"8e26413dad1890d45502dd31a75f9c403eee2fef" -> "54378aec6a6ea34638ac687217745e574360285e"
	"8e26413dad1890d45502dd31a75f9c403eee2fef" -> "6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92"
	"8e26413dad1890d45502dd31a75f9c403eee2fef" -> f9f2794a3dae393bdb07affde1719aee32e6c236
	"8e26413dad1890d45502dd31a75f9c403eee2fef" [label="8e26413" fillcolor="#bc9b8f"]
	"origin/HEAD" -> "origin/master"
	"origin/HEAD" [label=HEAD fillcolor="#ffbeb3"]
	"origin/idea1" -> "01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8"
	"origin/idea1" -> idea1
	"origin/idea1" [label=idea1 fillcolor="#ffa366"]
	"origin/master" -> "3447a63ea27b15856a751c3f631546ad6c98d07a"
	"origin/master" -> master
	"origin/master" [label=master fillcolor="#ffa366"]
	"v0.0.1" -> c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834
	"v0.0.1" [label="v0.0.1" fillcolor="#ffc61a"]
	"v0.0.2" -> b7cd4c5e269572826551e2358805684d23e9b187
	"v0.0.2" [label="v0.0.2" fillcolor="#ffc61a"]
	HEAD -> idea1
	HEAD [label=HEAD fillcolor="#e6ccff"]
	b7cd4c5e269572826551e2358805684d23e9b187 -> "3447a63ea27b15856a751c3f631546ad6c98d07a"
	b7cd4c5e269572826551e2358805684d23e9b187 [label=b7cd4c5 fillcolor="#ffdf80"]
	c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834 -> e04c9e73c27f423fecb1d8220c4a4b5ca217f2de
	c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834 -> e53574e083bfb447086df95ad1214d87b6ae45c4
	c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834 [label=c99b362 fillcolor="#85d5fa"]
	e04c9e73c27f423fecb1d8220c4a4b5ca217f2de -> "2358d7dee4b70234fb7078d735a835673dc4b45b"
	e04c9e73c27f423fecb1d8220c4a4b5ca217f2de -> ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8
	e04c9e73c27f423fecb1d8220c4a4b5ca217f2de [label=e04c9e7 fillcolor="#bc9b8f"]
	e53574e083bfb447086df95ad1214d87b6ae45c4 -> "737c972823aec2a30e726cd39821edf8d4b4826b"
	e53574e083bfb447086df95ad1214d87b6ae45c4 [label=e53574e fillcolor="#85d5fa"]
	ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8 [label=ecf7586 fillcolor="#9ccc66"]
	f9f2794a3dae393bdb07affde1719aee32e6c236 [label=f9f2794 fillcolor="#9ccc66"]
	idea1 -> "01ccfc8a7031f57c92a694c727fc16a1b6f6a3c8"
	idea1 [label=idea1 fillcolor="#9999ff"]
	idea2 -> c99b3621c6f61f36a468d9da2f2f4cb6c2c7f834
	idea2 [label=idea2 fillcolor="#9999ff"]
	master -> "3447a63ea27b15856a751c3f631546ad6c98d07a"
	master [label=master fillcolor="#9999ff"]
	origin -> "origin/HEAD"
	origin -> "origin/idea1"
	origin -> "origin/master"
	origin [label=origin fillcolor="#ff6666"]
}
"""
