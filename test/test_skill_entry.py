import unittest
from ovos_skills_manager.skill_entry import SkillEntry


# TODO setup a test skill repo, since a random url can simply vanish or be
#  modified


class TestGithubBranchParsing(unittest.TestCase):

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

