import pathlib

import pytest

import git_graph.cli as cli

tests_data_path = pathlib.Path(__file__).parent / 'data'

git_repos = ['minimal_repo',
             'full_repo',
             'remote_repo']


@pytest.mark.parametrize("git_repo", git_repos, ids=git_repos)
def test_repo(git_repo):
    git_repo_path = tests_data_path / git_repo

    # mandatory as git considers subfolders with .git inside as submodules
    old_git = git_repo_path / '.gitZ'
    new_git = git_repo_path / '.git'
    old_git.rename(new_git)

    args = ['-p', str(git_repo_path), '-c']

    output_file = cli.main(args)

    git_graph_path = git_repo_path / '.gitGraph'
    image_file = git_graph_path / output_file
    dot_file = git_graph_path / image_file.stem

    with open(dot_file) as f:
        dot_graph = f.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        with open(git_graph_path / 'expected.dot') as expected_dot_graph:
            assert ''.join(dot_graph) == expected_dot_graph.read()

    pathlib.Path.unlink(image_file)
    pathlib.Path.unlink(dot_file)

    new_git.rename(old_git)
