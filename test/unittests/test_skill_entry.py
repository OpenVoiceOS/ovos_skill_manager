import os
import sys
import unittest
from os.path import basename

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestSkillEntryFromGit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("GITHUB_TOKEN"):
            from ovos_skills_manager.session import set_github_token
            set_github_token(os.environ.get("GITHUB_TOKEN"))

    def test_requirements_from_txt(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/dev")
        self.assertIsInstance(entry.requirements, dict)
        self.assertIsInstance(entry.requirements["python"], list)

    def test_requirements_json_manifest_txt_dep_system_reqs(self):
        from ovos_skills_manager.skill_entry import SkillEntry
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
        from ovos_skills_manager.skill_entry import SkillEntry
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
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertIsInstance(entry.requirements["system"]["all"], list)

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "v0.2.1")
        self.assertEqual(entry.download_url, "https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/v0.2.1.zip")
        self.assertIsInstance(entry.uuid, str)
        self.assertEqual(entry.uuid, "tskill-osm_parsing.openvoiceos")

    def test_explicit_branch(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@dev")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertIsInstance(entry.requirements["python"], list)
        self.assertIsInstance(entry.requirements["system"], dict)
        self.assertIsInstance(entry.requirements["skill"], list)

        self.assertEqual(entry.branch, "dev")
        self.assertEqual(entry.download_url, "https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/dev.zip")
        self.assertIsInstance(entry.uuid, str)
        self.assertEqual(entry.uuid, "tskill-osm_parsing.openvoiceos")

    def test_equivalent_branch_specs(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        tree_spec = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/dev")
        at_spec = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@dev")
        self.assertEqual(tree_spec, at_spec)

    def test_equivalent_default(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        implicit = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        explicit = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/archive/v0.2.1.zip")
        self.assertEqual(implicit, explicit)

    def test_requirements_commented(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@commented_requirements")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertIsInstance(entry.requirements["python"], list)
        self.assertIsInstance(entry.requirements["system"], dict)
        self.assertIsInstance(entry.requirements["skill"], list)

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

    def test_requirements_null_json(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@commented_requirements")
        requirements = entry.json.pop("requirements")
        self.assertEqual(requirements, entry.requirements)

        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1")
        requirements = entry.json.pop("requirements")
        self.assertEqual(requirements, entry.requirements)

        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        requirements = entry.json.pop("requirements")
        self.assertEqual(requirements, entry.requirements)

    def test_skill_entry_uuid(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry.from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@dev")
        self.assertEqual(entry.uuid, "tskill-osm_parsing.openvoiceos")

        entry = SkillEntry.from_github_url("https://github.com/NeonDaniel/Tskill-osm_parsing@dev")
        self.assertEqual(entry.uuid, "tskill-osm_parsing.neondaniel")

    # TODO: Find a good method for parsing versions in requirements; for now, requirements installer should handle
    #       compatible versions, this just needs to handle incompatible versions
    # def test_requirements_mismatch_versions(self):
    #     from ovos_skills_manager.skill_entry import SkillEntry
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


class TestSkillEntryFromJson(unittest.TestCase):
    # TODO: Add some valid and invalid JSON to parse
    def test_skill_entry_properties_invalid_entry(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        entry = SkillEntry({})
        self.assertFalse(entry.uuid)
        self.assertIsInstance(entry.json, dict)
        self.assertIsInstance(repr(entry), str)
        self.assertEqual(entry, SkillEntry({}))


class TestSkillEntryFromDirectory(unittest.TestCase):
    def test_skill_entry_from_directory(self):
        from ovos_skills_manager.skill_entry import SkillEntry
        test_dir = os.path.join(os.path.dirname(__file__), "skill_dirs")
        complete_dir = os.path.join(test_dir, "tskill-osm_parsing-complete")
        minimal_dir = os.path.join(test_dir, "tskill-osm_parsing-minimal")
        no_git_dir = os.path.join(test_dir, "tskill-osm_parsing-no_git")
        no_json_dir = os.path.join(test_dir, "tskill-osm_parsing-no_json")


        with self.assertRaises(ValueError):
            SkillEntry.from_directory(__file__)
        with self.assertRaises(ValueError):
            SkillEntry.from_directory("/invalid")

        for test_skill_dir in (complete_dir, minimal_dir, no_git_dir, no_json_dir):
            skill = SkillEntry.from_directory(test_skill_dir)
            self.assertIsInstance(skill, SkillEntry)
            self.assertIsInstance(skill.uuid, str)
            self.assertEqual(skill.appstore, "InstalledSkills")
            self.assertIsInstance(skill.skill_name, str)
            self.assertEqual(skill.skill_folder, basename(test_skill_dir))
            self.assertIsInstance(skill.skill_examples, list)
            self.assertIsInstance(skill.requirements, dict)
            self.assertIsInstance(skill.url, str)

            if test_skill_dir == complete_dir:
                self.assertTrue(skill.url.startswith("https://github.com"))
                self.assertEqual(set(skill.requirements["python"]),
                                 {"text_requirements",
                                  "manifest_requirement",
                                  "json-requirements"})
                self.assertIsInstance(skill.requirements["system"], dict)
                self.assertEqual(set(skill.requirements["skill"]),
                                 {"manifest-skill",
                                  "json-skill"})
            elif test_skill_dir == minimal_dir:
                self.assertEqual(set(skill.requirements["python"]),
                                 {"text_requirements"})
                self.assertIsInstance(skill.requirements["system"], dict)
            elif test_skill_dir == no_git_dir:
                self.assertEqual(set(skill.requirements["python"]),
                                 {"text_requirements",
                                  "manifest_requirement",
                                  "json-requirements"})
                self.assertIsInstance(skill.requirements["system"], dict)
                self.assertEqual(set(skill.requirements["skill"]),
                                 {"manifest-skill",
                                  "json-skill"})
            elif test_skill_dir == no_json_dir:
                self.assertEqual(set(skill.requirements["python"]),
                                 {"text_requirements",
                                  "manifest_requirement"})
                self.assertIsInstance(skill.requirements["system"], dict)
                self.assertEqual(set(skill.requirements["skill"]),
                                 {"manifest-skill"})


if __name__ == '__main__':
    unittest.main()
