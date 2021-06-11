import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.osm import OVOSSkillsManager

osm = OVOSSkillsManager()


class TestOvosSkillsManager(unittest.TestCase):

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
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
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
                         {"json-requirements", "manifest_requirement", "text_requirements"})
        self.assertIsInstance(skill_entry.requirements["system"], dict)
        self.assertIsInstance(skill_entry.requirements["skill"], list)
        self.assertIsInstance(skill_entry.download_url, str)
        self.assertTrue(skill_entry.download_url.endswith("/v0.1.1.zip"))


if __name__ == "__main__":
    unittest.main()
