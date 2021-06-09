import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ovos_skills_manager.github import \
    get_branch_from_github_url, get_branch_from_skill_json_github_url, \
    get_branch_from_latest_release_github_url
from ovos_skills_manager.exceptions import GithubInvalidBranch, \
    GithubFileNotFound


# TODO setup a test skill repo, since a random url can simply vanish or be
#  modified


class TestGithubBranchParsing(unittest.TestCase):
    def test_get_branch_from_url_invalid(self):
        with self.assertRaises(GithubInvalidBranch):
            get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test")
        with self.assertRaises(GithubInvalidBranch):
            get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/INVALID_BRANCH", True)
        with self.assertRaises(GithubInvalidBranch):
            get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test@INVALID_BRANCH", True)

    def test_get_branch_from_url_tree(self):
        self.assertEqual(get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/v0.1", True),
                         "v0.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/v0.1.1", True),
                         "v0.1.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/master", True),
                         "master")

    def test_get_branch_from_url_at(self):
        self.assertEqual(get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test@v0.1", True),
                         "v0.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test@v0.1.1", True),
                         "v0.1.1")
        self.assertEqual(get_branch_from_github_url("https://github.com/NeonDaniel/skill-osm-test@master", True),
                         "master")

    def test_get_branch_from_commit(self):
        self.assertEqual(get_branch_from_github_url(
            "https://github.com/NeonDaniel/skill-osm-test/commit/06fabb262077d80c32ffd12ed1092bb914658067", True),
            "06fabb262077d80c32ffd12ed1092bb914658067")

    def test_get_branch_from_blob(self):
        self.assertEqual(get_branch_from_github_url(
            "https://github.com/NeonDaniel/skill-osm-test/blob/v0.1/skill.json", True), "v0.1")

    def test_branch_from_json_default_branch(self):
        self.assertEqual(get_branch_from_skill_json_github_url("https://github.com/NeonDaniel/skill-osm-test"), "v0.1")

    def test_branch_from_json_matching_branch(self):
        self.assertEqual(get_branch_from_skill_json_github_url("https://github.com/NeonDaniel/skill-osm-test@v0.1"),
                         "v0.1")

    def test_branch_from_json_not_matching_branch(self):
        self.assertEqual(get_branch_from_skill_json_github_url("https://github.com/NeonDaniel/skill-osm-test@v0.1.1"),
                         "v0.1")

    def test_branch_from_latest_release(self):
        latest = "v0.1.1"

        default = get_branch_from_latest_release_github_url("https://github.com/NeonDaniel/skill-osm-test")
        self.assertEqual(default, latest)
        old_release = get_branch_from_latest_release_github_url("https://github.com/NeonDaniel/skill-osm-test@v0.1")
        self.assertEqual(old_release, latest)
        dev_branch = get_branch_from_latest_release_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/dev")
        self.assertEqual(dev_branch, latest)

    def test_branch_from_json_invalid(self):
        with self.assertRaises(GithubFileNotFound):
            get_branch_from_skill_json_github_url("https://github.com/NeonDaniel/skill-osm-test/tree/no_json")
        with self.assertRaises(GithubFileNotFound):
            get_branch_from_skill_json_github_url("https://github.com/NeonDaniel/skill-osm-test@no_json")


if __name__ == '__main__':
    unittest.main()
