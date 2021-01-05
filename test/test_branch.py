import unittest
from ovos_skills_manager.github import get_branch_from_github_releases, \
    get_branch_from_github_url, get_branch_from_skill_json_github_url, \
    get_branch_from_skill_json, get_branch_from_github_api, get_branch, \
    get_branch_from_skill_json_github_api, \
    get_branch_from_latest_release_github_url
from ovos_skills_manager.exceptions import GithubInvalidBranch, \
    GithubFileNotFound


# TODO setup a test skill repo, since a random url can simply vanish or be
#  modified


class TestGithubBranchParsing(unittest.TestCase):

    def test_url(self):
        url_no_branch = "https://github.com/JarbasSkills/skill-ddg"
        url_branch = "https://github.com/JarbasSkills/skill-ddg/tree/v0.1.0"
        blob_url = "https://github.com/OpenVoiceOS/OVOS-skills-store/blob" \
                   "/f4ab4ea00e47955798c9906c8c03807391bc20f0/skill-icanhazdadjokes.json"

        self.assertEqual(get_branch_from_github_url(url_branch), "v0.1.0")
        self.assertEqual(get_branch_from_github_url(blob_url),
                         "f4ab4ea00e47955798c9906c8c03807391bc20f0")
        self.assertRaises(
            GithubInvalidBranch, get_branch_from_github_url, url_no_branch
        )

    def test_json(self):
        master = "https://github.com/JarbasSkills/skill-ddg"
        v03 = "https://github.com/JarbasSkills/skill-dagon"
        url_branch = "https://github.com/JarbasSkills/skill-dagon/tree/v0.2"
        json_url = "https://github.com/OpenVoiceOS/OVOS-skills-store/blob/f4ab4ea00e47955798c9906c8c03807391bc20f0/skill-icanhazdadjokes.json"
        no_json = "https://github.com/mycroftai/skill-hello-world"
        no_json_url = "https://github.com/mycroftai/skill-hello-world/tree/20.02"
        self.assertEqual(get_branch_from_skill_json_github_url(master),
                         "master")
        self.assertEqual(get_branch_from_skill_json_github_url(v03),
                         "v0.3.0")
        self.assertEqual(get_branch_from_skill_json_github_url(url_branch),
                         "v0.2")
        self.assertEqual(get_branch_from_skill_json_github_url(json_url),
                         "v0.1.0")
        self.assertRaises(
            GithubFileNotFound, get_branch_from_skill_json_github_url, no_json
        )
        self.assertRaises(GithubFileNotFound,
                          get_branch_from_skill_json_github_url, no_json_url
                          )

    def test_release(self):
        master = "https://github.com/JarbasSkills/skill-ddg"
        v03 = "https://github.com/JarbasSkills/skill-dagon"
        url_branch = "https://github.com/JarbasSkills/skill-dagon/tree/v0.2"
        no_release = "https://github.com/mycroftai/skill-hello-world"
        self.assertEqual(get_branch_from_latest_release_github_url(master),
                         "v0.1.0")
        self.assertEqual(get_branch_from_latest_release_github_url(v03),
                         "v0.2.1")
        self.assertEqual(get_branch_from_latest_release_github_url(url_branch),
                         "v0.2.1")
        self.assertRaises(GithubFileNotFound,
                          get_branch_from_latest_release_github_url, no_release
                          )
