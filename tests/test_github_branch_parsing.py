import os
import sys
import unittest



class TestGithubBranchParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))

        if os.environ.get("GITHUB_TOKEN"):
            from ovos_skills_manager.session import set_github_token
            set_github_token(os.environ.get("GITHUB_TOKEN"))

        # TODO setup a test skill repo, since a random url can simply vanish or be
        #  modified

    def test_get_branch_from_url_invalid(self):
        from ovos_skills_manager.exceptions import GithubInvalidBranch
        from ovos_skills_manager.github import get_branch_from_github_url
        with self.assertRaises(GithubInvalidBranch):
            get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        with self.assertRaises(GithubInvalidBranch):
            get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/INVALID_BRANCH", True)
        with self.assertRaises(GithubInvalidBranch):
            get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@INVALID_BRANCH", True)

    def test_get_branch_from_url_tree(self):
        from ovos_skills_manager.github import get_branch_from_github_url
        self.assertEqual(get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/v0.2.1", True),
                         "v0.2.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/v0.2.1", True),
                         "v0.2.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/master", True),
                         "master")

    def test_get_branch_from_url_at(self):
        from ovos_skills_manager.github import get_branch_from_github_url
        self.assertEqual(get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1", True),
                         "v0.2.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1", True),
                         "v0.2.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@master", True),
                         "master")

    def test_get_branch_from_commit(self):
        from ovos_skills_manager.github import get_branch_from_github_url
        self.assertEqual(get_branch_from_github_url(
            "https://github.com/OpenVoiceOS/tskill-osm_parsing/commit/06fabb262077d80c32ffd12ed1092bb914658067", True),
            "06fabb262077d80c32ffd12ed1092bb914658067")

    def test_get_branch_from_blob(self):
        from ovos_skills_manager.github import get_branch_from_github_url
        self.assertEqual(get_branch_from_github_url(
            "https://github.com/OpenVoiceOS/tskill-osm_parsing/blob/v0.2.1/skill.json", True), "v0.2.1")

    def test_branch_from_json_default_branch(self):
        from ovos_skills_manager.github import get_branch_from_skill_json_github_url
        self.assertEqual(get_branch_from_skill_json_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing"), "v0.2.1")

    def test_branch_from_json_matching_branch(self):
        from ovos_skills_manager.github import get_branch_from_skill_json_github_url
        self.assertEqual(get_branch_from_skill_json_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1"),
                         "v0.2.1")

    def test_branch_from_json_not_matching_branch(self):
        from ovos_skills_manager.github import get_branch_from_skill_json_github_url
        self.assertEqual(get_branch_from_skill_json_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1"),
                         "v0.2.1")

    def test_branch_from_latest_release(self):
        from ovos_skills_manager.github import get_branch_from_latest_release_github_url

        latest = "v0.2.1"

        default = get_branch_from_latest_release_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing")
        self.assertEqual(default, latest)
        old_release = get_branch_from_latest_release_github_url(
            "https://github.com/OpenVoiceOS/tskill-osm_parsing@v0.2.1")
        self.assertEqual(old_release, latest)
        dev_branch = get_branch_from_latest_release_github_url(
            "https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/dev")
        self.assertEqual(dev_branch, latest)

    def test_branch_from_json_invalid(self):
        from ovos_skills_manager.github import get_branch_from_skill_json_github_url, GithubFileNotFound
        with self.assertRaises(GithubFileNotFound):
            get_branch_from_skill_json_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing/tree/no_json")
        with self.assertRaises(GithubFileNotFound):
            get_branch_from_skill_json_github_url("https://github.com/OpenVoiceOS/tskill-osm_parsing@no_json")


if __name__ == '__main__':
    unittest.main()
