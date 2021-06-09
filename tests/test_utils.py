import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.utils import *


class TestSkillEntry(unittest.TestCase):
    def test_parse_python_dependencies_no_auth(self):
        test_input = ["package~=0.1",
                      "package~=0.2",
                      "git_dep @ git+https://github.com/myUser/SecretDependency@Branch"]
        valid_output = ["package~=0.1",
                        "package~=0.2",
                        "git_dep @ git+https://github.com/myuser/secretdependency@Branch"]
        self.assertEqual(parse_python_dependencies(test_input), valid_output)

    def test_parse_python_dependencies_with_auth(self):
        test_input = ["package~=0.1",
                      "package~=0.2",
                      "git_dep @ git+https://github.com/myUser/SecretDependency@Branch"]
        valid_output = ["package~=0.1",
                        "package~=0.2",
                        "git_dep @ git+https://TOKEN@github.com/myuser/secretdependency@Branch"]
        self.assertEqual(parse_python_dependencies(test_input, "TOKEN"), valid_output)

    # TODO: Test Readme/Desktop to json methods


if __name__ == '__main__':
    unittest.main()
