import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.skill_entry import SkillEntry


class TestSkillEntry(unittest.TestCase):
    def test_requirements_from_txt(self):
        entry = SkillEntry.from_github_url("https://github.com/NeonGeckoCom/speed-test.neon/tree/dev")
        self.assertIsInstance(entry.requirements, dict)
        self.assertIsInstance(entry.requirements["python"], list)

    def test_requirements_json_manifest_txt_dep_system_reqs(self):
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/v0.1")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertIsInstance(entry.requirements["system"]["all"], str)  # Depreciated Behavior!

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "v0.1")
        self.assertEqual(entry.download_url, "https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/v0.1.zip")

    def test_requirements_json_manifest_txt(self):
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/main")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertEqual(set(entry.requirements["system"]["all"]),
                         {"json-pkg", "system-manifest-pkg"})

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "main")
        self.assertEqual(entry.download_url, "https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/main.zip")

    def test_implicit_branch(self):
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertIsInstance(entry.requirements["system"]["all"], str)

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "v0.1")
        self.assertEqual(entry.download_url, "https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/v0.1.zip")
        self.assertIsInstance(entry.uuid, str)

    def test_explicit_branch(self):
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@dev")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertIsInstance(entry.requirements["python"], list)
        self.assertIsInstance(entry.requirements["system"], dict)
        self.assertIsInstance(entry.requirements["skill"], list)

        self.assertEqual(entry.branch, "dev")
        self.assertEqual(entry.download_url, "https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/dev.zip")
        self.assertIsInstance(entry.uuid, str)

    def test_equivalent_branch_specs(self):
        tree_spec = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/dev")
        at_spec = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@dev")
        self.assertEqual(tree_spec, at_spec)

    def test_equivalent_default(self):
        implicit = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        explicit = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/v0.1.zip")
        self.assertEqual(implicit, explicit)

    def test_requirements_commented(self):
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@commented_requirements")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertIsInstance(entry.requirements["python"], list)
        self.assertIsInstance(entry.requirements["system"], dict)
        self.assertIsInstance(entry.requirements["skill"], list)

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

    def test_requirements_null_json(self):
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@commented_requirements")
        requirements = entry.json.pop("requirements")
        self.assertEqual(requirements, entry.requirements)

        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.1")
        requirements = entry.json.pop("requirements")
        self.assertEqual(requirements, entry.requirements)

        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        requirements = entry.json.pop("requirements")
        self.assertEqual(requirements, entry.requirements)

    def test_skill_entry_properties_invalid_entry(self):
        entry = SkillEntry({})
        self.assertIsNone(entry.uuid)
        self.assertIsInstance(entry.json, dict)
        self.assertIsInstance(repr(entry), str)
        self.assertEqual(entry, SkillEntry({}))

    # TODO: Find a good method for parsing versions in requirements; for now, requirements installer should handle
    #       compatible versions, this just needs to handle incompatible versions
    # def test_requirements_mismatch_versions(self):
    #     entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@conflicting_requirements")
    #     self.assertIsInstance(entry.requirements, dict)
    #     self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})
    #
    #     self.assertIsInstance(entry.requirements["python"], list)
    #     self.assertIsInstance(entry.requirements["system"], dict)
    #     self.assertIsInstance(entry.requirements["skill"], list)
    #
    #     self.assertEqual(set(entry.requirements["python"]),
    #                      {"json-requirements", "manifest_requirement", "text_requirements", "awesome-pkg~=1.1"})


if __name__ == '__main__':
    unittest.main()
