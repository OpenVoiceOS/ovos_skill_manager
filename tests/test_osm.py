import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.osm import OVOSSkillsManager
from ovos_skills_manager.session import set_github_token
osm = OVOSSkillsManager()


class TestOvosSkillsManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            set_github_token(github_token)

    def test_get_skill_entry_from_url_default_branch(self):
        from ovos_skills_manager import SkillEntry

        skill_entry = osm.skill_entry_from_url("https://github.com/NeonDaniel/skill-osm-test")
        self.assertIsInstance(skill_entry, SkillEntry)
        self.assertEqual(skill_entry.url, "https://github.com/NeonDaniel/skill-osm-test")
        self.assertIsInstance(skill_entry.requirements["python"], list)
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/main.zip"))

    def test_get_skill_entry_from_url_no_json(self):
        from ovos_skills_manager import SkillEntry

        skill_entry = osm.skill_entry_from_url("https://github.com/NeonDaniel/skill-osm-test/tree/no_json")
        self.assertIsInstance(skill_entry, SkillEntry)
        self.assertEqual(skill_entry.url, "https://github.com/NeonDaniel/skill-osm-test")
        self.assertEqual(skill_entry.branch, "no_json")
        self.assertIsInstance(skill_entry.requirements["python"], list)
        self.assertTrue(len(skill_entry.requirements["python"]) > 0)
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertTrue(len(skill_entry.requirements["system"].keys()) > 0)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertTrue(len(skill_entry.requirements["skill"]) > 0)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/no_json.zip"))

    def test_get_skill_entry_from_url_release(self):
        from ovos_skills_manager import SkillEntry

        skill_entry = osm.skill_entry_from_url("https://github.com/NeonDaniel/skill-osm-test@v0.1.1")
        self.assertIsInstance(skill_entry, SkillEntry)
        self.assertEqual(skill_entry.url, "https://github.com/NeonDaniel/skill-osm-test")
        self.assertEqual(skill_entry.branch, "v0.1.1")
        self.assertIsInstance(skill_entry.requirements["python"], list)
        self.assertEqual(set(skill_entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"},
                         repr(set(skill_entry.requirements["python"])))
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/v0.1.1.zip"))


if __name__ == "__main__":
    unittest.main()
