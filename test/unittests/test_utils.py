import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class TestSkillEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("GITHUB_TOKEN"):
            from ovos_skills_manager.session import set_github_token
            set_github_token(os.environ.get("GITHUB_TOKEN"))

    def test_parse_python_dependencies_no_auth(self):
        from ovos_skills_manager.utils import parse_python_dependencies
        test_input = ["package~=0.1",
                      "package~=0.2",
                      "git_dep @ git+https://github.com/myUser/SecretDependency@Branch"]
        valid_output = ["package~=0.1",
                        "package~=0.2",
                        "git_dep @ git+https://github.com/myuser/secretdependency@Branch"]
        self.assertEqual(parse_python_dependencies(test_input), valid_output)

    def test_parse_python_dependencies_with_auth(self):
        from ovos_skills_manager.utils import parse_python_dependencies
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
