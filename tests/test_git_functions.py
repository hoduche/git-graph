import git_graph.git_functions as gf

good_path = 'examples/branch'
wrong_path_1 = 'examples3/branch'
wrong_path_2 = 'examples/branch3'
good_git_file_1 = '3d06bbd'
good_git_file_2 = '1b44346'
wrong_git_file = '1b44345'


#def test_read_git_file():
#    result = ['tree c943c1c80b10a4d18c4852df760ec8ab123d0453',
#              'author Henri-Olivier Duche <Henri-Olivier Duche> 1545516693 +0100',
#              'committer Henri-Olivier Duche <Henri-Olivier Duche> 1545516693 +0100',
#              '',
#              'commit number 1']
#    assert gf.read_git_file(good_path, good_git_file_1) == result
##    assert gf.read_git_file(good_path, wrong_git_file) is None
##    assert gf.read_git_file(wrong_path_1, good_git_file_1) == None
#
#
#def test_get_git_objects():
#    blobs, trees, commits, annotated_tags = gf.get_git_objects(good_path)
#    assert blobs == ['6b584e8ece562ebffc15d38808cd6b98fc3d97ea',
#                     'd07ef4424e9caea50099ea1858d3c98c01ece186']
#    assert trees == ['704f9d223bc6288206baeb6b9436634e29fb504c',
#                     'c943c1c80b10a4d18c4852df760ec8ab123d0453']
#    assert commits == ['3d06bbd356e15d9bc2de7e3a6d23311428f90f55',
#                       'd3902329e10a9ed5ff0426eebada3f9c1d01c5cd']
#    assert annotated_tags == ['1b44346eb575773cbbd80644a3e94210afadb6a8',
#                              '4bcf55466d35fa5c17a06300dc256df02b9d3ca1',
#                              'aee3d18ffc66bab391b4a636118dc669bac2fd27']
