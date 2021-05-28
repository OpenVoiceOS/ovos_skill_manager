import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.skill_entry import SkillEntry


# TODO setup a test skill repo, since a random url can simply vanish or be
#  modified


class TestSkillEntry(unittest.TestCase):
    def test_requirements_from_txt(self):
        entry = SkillEntry.from_github_url("https://github.com/NeonGeckoCom/speed-test.neon/tree/dev")
        self.assertIsInstance(entry.requirements, dict)
        self.assertIsInstance(entry.requirements["python"], list)

    def test_requirements_json_manifest_txt_dep_system_reqs(self):
        entry = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/v0.1")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertIsInstance(entry.requirements["system"]["all"], str)  # Depreciated Behavior!

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "v0.1")
        self.assertEqual(entry.download_url, "https://github.com/NeonDaniel/skill-osm-test/archive/v0.1.zip")

    def test_requirements_json_manifest_txt(self):
        entry = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/main")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertEqual(set(entry.requirements["system"]["all"]),
                         {"json-pkg", "system-manifest-pkg"})

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "main")
        self.assertEqual(entry.download_url, "https://github.com/NeonDaniel/skill-osm-test/archive/main.zip")

    def test_implicit_branch(self):
        entry = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertEqual(set(entry.requirements["python"]),
                         {"json-requirements", "manifest_requirement", "text_requirements"})

        self.assertEqual(set(entry.requirements["system"]["all"]),
                         {"json-pkg", "system-manifest-pkg"})

        self.assertEqual(set(entry.requirements["skill"]),
                         {"json-skill", "manifest-skill"})

        self.assertEqual(entry.branch, "v0.1")
        self.assertEqual(entry.download_url, "https://github.com/NeonDaniel/skill-osm-test/archive/v0.1.zip")

    def test_explicit_branch(self):
        entry = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test@dev")
        self.assertIsInstance(entry.requirements, dict)
        self.assertEqual(set(entry.requirements.keys()), {"python", "system", "skill"})

        self.assertIsInstance(entry.requirements["python"], list)
        self.assertIsInstance(entry.requirements["system"], dict)
        self.assertIsInstance(entry.requirements["skill"], list)

        self.assertEqual(entry.branch, "dev")
        self.assertEqual(entry.download_url, "https://github.com/NeonDaniel/skill-osm-test/archive/dev.zip")

    def test_equivalent_branch_specs(self):
        tree_spec = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/dev")
        at_spec = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test@dev")
        self.assertEqual(tree_spec, at_spec)

    def test_equivalent_default(self):
        implicit = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test")
        explicit = SkillEntry.from_github_url("https://github.com/NeonDaniel/skill-osm-test/archive/v0.1.zip")
        self.assertEqual(implicit, explicit)

    def test_url(self):
        branch_from_json = "https://github.com/JarbasSkills/skill-bandcamp"
        branch_from_tree = "https://github.com/JarbasSkills/skill-ddg/tree/v0.1.0"
        commit_from_blob = "https://github.com/OpenVoiceOS/OVOS-skills-store/blob" \
                           "/f4ab4ea00e47955798c9906c8c03807391bc20f0/skill-icanhazdadjokes.json"
        branch_from_git = "https://github.com/NeonGeckoCom/caffeinewiz.neon@dev"

        # should get branch defined in https://github.com/JarbasSkills/skill-ddg/blob/master/res/desktop/skill.json
        entry = SkillEntry.from_github_url(branch_from_json)
        self.assertEqual(entry.branch, "v0.3.1")

        # should match commit pinned in url
        entry = SkillEntry.from_github_url(commit_from_blob)
        self.assertEqual(entry.branch, "f4ab4ea00e47955798c9906c8c03807391bc20f0")

        # dev branch implicit in url
        entry = SkillEntry.from_github_url(branch_from_git)
        self.assertEqual(entry.branch, "dev")

        # github release implicit in url
        entry = SkillEntry.from_github_url(branch_from_tree)
        self.assertEqual(entry.branch, "v0.1.0")


if __name__ == '__main__':
    unittest.main()
