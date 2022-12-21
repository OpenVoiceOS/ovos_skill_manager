import os
import sys
import unittest
import importlib
import json

from unittest.mock import Mock
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("GITHUB_TOKEN"):
            from ovos_skills_manager.session import set_github_token
            set_github_token(os.environ.get("GITHUB_TOKEN"))

    def test_parse_python_dependencies(self):
        from ovos_skills_manager.utils import parse_python_dependencies

        # No Auth
        test_input = ["package~=0.1",
                      "package~=0.2",
                      "git_dep @ git+https://github.com/myUser/SecretDependency@Branch"]
        valid_output = ["package~=0.1",
                        "package~=0.2",
                        "git_dep @ git+https://github.com/myuser/secretdependency@Branch"]
        self.assertEqual(parse_python_dependencies(test_input), valid_output)

        # With Auth
        test_input = ["package~=0.1",
                      "package~=0.2",
                      "git_dep @ git+https://github.com/myUser/SecretDependency@Branch"]
        valid_output = ["package~=0.1",
                        "package~=0.2",
                        "git_dep @ git+https://TOKEN@github.com/myuser/secretdependency@Branch"]
        self.assertEqual(parse_python_dependencies(test_input, "TOKEN"), valid_output)

    def test_readme_to_json(self):
        pass

    def test_desktop_to_json(self):
        pass

    def test_build_skills_list(self):
        pass

    def test_read_skill_json(self):
        pass

    def test_read_skill_examples(self):
        pass

    def test_get_skills_info(self):
        pass

    def test_get_skills_examples(self):
        pass

    def test_get_skills_from_url(self):
        from ovos_skills_manager.utils import get_skills_from_url
        test_url = 'https://raw.githubusercontent.com/NeonGeckoCom/neon_skills/' \
                   '606421bb3e9b3436ab3ca1a6bc51476f67e0e09a/' \
                   'skill_lists/DEFAULT-SKILLS'
        skills = get_skills_from_url(test_url)
        self.assertIsInstance(skills, list)
        self.assertTrue(all((x.startswith('https://github.com')
                             for x in skills)))

    def test_set_osm_constraints_file(self):
        import ovos_skills_manager.requirements
        from ovos_skills_manager.utils import set_osm_constraints_file
        set_osm_constraints_file(__file__)
        self.assertEqual(ovos_skills_manager.requirements.DEFAULT_CONSTRAINTS,
                         __file__)

    def test_get_pypi_version(self):
        from ovos_skills_manager.utils import get_pypi_package_versions
        versions = get_pypi_package_versions("neon-skill-about")
        self.assertIsInstance(versions, list)

    def test_install_local_skill_dependencies(self):
        import ovos_skills_manager.requirements
        from ovos_skills_manager.utils import install_local_skill_dependencies
        install_pip_deps = Mock()
        install_sys_deps = Mock()
        ovos_skills_manager.requirements.pip_install = install_pip_deps
        ovos_skills_manager.requirements.install_system_deps = install_sys_deps

        local_skills_dir = os.path.join(os.path.dirname(__file__),
                                        "local_skills")

        installed = install_local_skill_dependencies(local_skills_dir)
        num_installed = len(installed)
        self.assertEqual(installed, os.listdir(local_skills_dir))
        self.assertEqual(num_installed, install_pip_deps.call_count)
        self.assertEqual(num_installed, install_sys_deps.call_count)


if __name__ == '__main__':
    unittest.main()
