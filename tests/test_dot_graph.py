import os
import pathlib
import subprocess

import pytest

import git_graph.dot_graph as dg

tests_data_path = pathlib.Path(__file__).parent / 'data'

git_repo_types = [('minimal_repo', 4),
                  ('full_repo', 5),
                  ('remote_repo', 5)]

author = "Bernard"
email = "author@cie.com"
action_date = "Sat Oct 15 11:00 2011 +0100"
os.environ["GIT_AUTHOR_NAME"] = author
os.environ["GIT_COMMITTER_NAME"] = author
os.environ["GIT_AUTHOR_EMAIL"] = email
os.environ["GIT_COMMITTER_EMAIL"] = email
os.environ["GIT_AUTHOR_DATE"] = action_date
os.environ["GIT_COMMITTER_DATE"] = action_date


@pytest.fixture(params=git_repo_types, ids=[i[0] for i in git_repo_types])
def build_repo(request, tmp_path):
    git_repo_type = request.param[0]
    nb_files = request.param[1]
    if git_repo_type == 'minimal_repo':
        build_minimal_repo(tmp_path)
    elif git_repo_type == 'full_repo':
        build_full_repo(tmp_path)
    elif git_repo_type == 'remote_repo':
        build_remote_repo(tmp_path)
    return git_repo_type, nb_files, tmp_path


def test_repo(build_repo):
    git_repo_type, nb_files, tmp_path = build_repo

    output_file = dg.DotGraph(tmp_path).persist()

    git_graph_path = tmp_path / '.gitGraph'
    image_file = git_graph_path / output_file
    dot_file = git_graph_path / image_file.stem

    assert len(list(tmp_path.iterdir())) == nb_files
    assert git_graph_path.is_dir()
    assert len(list(git_graph_path.iterdir())) == 2

    with open(dot_file) as f:
        dot_graph = f.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        golden = tests_data_path / git_repo_type / '.gitGraph' / 'expected.dot'
        with open(golden) as expected_dot_graph:
            assert ''.join(dot_graph) == expected_dot_graph.read()


def execute_bash_command(path, command):
    try:
        subprocess.run(command.split(), cwd=str(path))
    except subprocess.CalledProcessError:
        print('Not a bash command')


def build_minimal_repo(tmp_path):
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


def build_full_repo(tmp_path):
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


def build_remote_repo(tmp_path):
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
