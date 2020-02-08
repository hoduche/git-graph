import os
import pathlib
import subprocess

import git_graph.dot_graph as dg

tests_path = pathlib.Path(__file__).parent

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
    output, error = subprocess.Popen(command.split(), cwd=str(path),
                                     stdout=subprocess.PIPE).communicate()
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
        with open(tests_path / 'minimal_repo.dot') as minimal_repo_dot_graph:
            assert ''.join(dot_graph) == minimal_repo_dot_graph.read()


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
        with open(tests_path / 'full_repo.dot') as full_repo_dot_graph:
            assert ''.join(dot_graph) == full_repo_dot_graph.read()


def test_remote_repo(tmp_path):
    # resume from full_repo
    # git tag v0.0.2 -am "good job"
    # git remote add origin https://github.com/hoduche/git-empty.git
    # git push -u origin master
    # git checkout idea1
    # git push -u origin idea1
    # git checkout master
    # git push origin --tags

    execute_bash_command(tmp_path,
                         'git clone https://github.com/hoduche/git-empty .')
    execute_bash_command(tmp_path, 'git checkout -b idea1 origin/idea1')
    execute_bash_command(tmp_path, 'git branch idea2 v0.0.1')

    dg.DotGraph(tmp_path).persist()
    dot_file_path = list((tmp_path / '.gitGraph').glob('*.dot'))[0]
    with open(dot_file_path) as dot_file:
        dot_graph = dot_file.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        with open(tests_path / 'remote_repo.dot') as remote_repo_dot_graph:
            assert ''.join(dot_graph) == remote_repo_dot_graph.read()
