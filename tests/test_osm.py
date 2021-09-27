import os
import shutil
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

TEST_INSTALL_DIR = os.path.join(os.path.dirname(__file__), "skills")

class TestOvosSkillsManager(unittest.TestCase):
    osm: object
    @classmethod
    def setUpClass(cls) -> None:
        from .conftest import OVOSSkillsManager
        cls.osm = OVOSSkillsManager()
        assert 'tmp' in cls.osm.config.path

        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            from ovos_skills_manager.session import set_github_token
            set_github_token(github_token)

    def setUp(self) -> None:
        if os.path.exists(TEST_INSTALL_DIR):
            shutil.rmtree(TEST_INSTALL_DIR)
        os.makedirs(TEST_INSTALL_DIR)

    def tearDown(self) -> None:
        if os.path.exists(TEST_INSTALL_DIR):
            shutil.rmtree(TEST_INSTALL_DIR)

    def test_get_skill_entry_from_url_default_branch(self):
        from ovos_skills_manager import SkillEntry

        skill_entry = self.osm.skill_entry_from_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertIsInstance(skill_entry, SkillEntry)
        self.assertEqual(skill_entry.url, "https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertIsInstance(skill_entry.requirements["python"], list)
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/main.zip"))
        self.assertIsInstance(skill_entry.uuid, str)

    def test_get_skill_entry_from_url_no_json(self):
        from ovos_skills_manager import SkillEntry

        skill_entry = self.osm.skill_entry_from_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/no_json")
        self.assertIsInstance(skill_entry, SkillEntry)
        self.assertEqual(skill_entry.url, "https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertEqual(skill_entry.branch, "no_json")
        self.assertIsInstance(skill_entry.requirements["python"], list)
        self.assertTrue(len(skill_entry.requirements["python"]) > 0)
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertTrue(len(skill_entry.requirements["system"].keys()) > 0)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertTrue(len(skill_entry.requirements["skill"]) > 0)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/no_json.zip"))
        self.assertIsInstance(skill_entry.uuid, str)

    def test_get_skill_entry_from_url_release(self):
        from ovos_skills_manager import SkillEntry

        skill_entry = self.osm.skill_entry_from_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1")
        self.assertIsInstance(skill_entry, SkillEntry)
        self.assertEqual(skill_entry.url, "https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertEqual(skill_entry.branch, "v0.2.1")
        self.assertIsInstance(skill_entry.requirements["python"], list)
        self.assertEqual(set(skill_entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"},
                         repr(set(skill_entry.requirements["python"])))
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/v0.2.1.zip"))
        self.assertIsInstance(skill_entry.uuid, str)

    def test_install_skill_from_url_valid(self):
        self.osm.install_skill_from_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@installable", TEST_INSTALL_DIR)
        self.assertTrue(os.path.isdir(os.path.join(TEST_INSTALL_DIR, "tskill-osm_parsing.openvoiceos")),
                        os.listdir(TEST_INSTALL_DIR))
        self.assertTrue(os.path.isfile(os.path.join(TEST_INSTALL_DIR, "tskill-osm_parsing.openvoiceos", "__init__.py")))


if __name__ == "__main__":
    unittest.main()
