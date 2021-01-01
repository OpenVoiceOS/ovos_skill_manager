import unittest
from ovos_skills_manager.github.utils import *

# TODO setup a test skill repo, since a random url can simply vanish


class TestGithubUrlParsing(unittest.TestCase):

    def test_normalize_url(self):
        normie = "https://github.com/JarbasSkills/skill-wolfie"
        raw = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie"
        api = "https://api.github.com/repos/JarbasSkills/skill-wolfie"
        urls = [
            normie, raw, api,
            normie + "/blob/master/__init__.py",
            normie + "/blob/v0.1/res/desktop/skill.json",
            raw + "/v0.1/res/desktop/skill.json",
            api + "/commits/09de4133f8d53230f93b61b5fd8e8267f4b0aec4",
            api + "/zipball/v0.1", api + "/tarball/v0.1"
        ]
        for url in urls:
            self.assertEqual(normalize_github_url(url), normie)

    def test_branch_from_url(self):
        normie = "https://github.com/MycroftAI/skill-hello-world"

        # implicit branch in url
        self.assertEqual(
            get_branch_from_github_url(normie + "/tree/20.08"), "20.08"
        )
        self.assertEqual(
            get_branch_from_github_url(normie + "/tree/20.02"), "20.02"
        )

        # missing branch
        self.assertRaises(
            GithubInvalidBranch, get_branch_from_github_url, normie
        )

    def test_author_repo_from_url(self):
        url = "https://github.com/JarbasSkills/skill-wolfie"
        self.assertEqual(author_repo_from_github_url(url),
                         ["JarbasSkills", "skill-wolfie"])
        self.assertEqual(author_repo_from_github_url(url + "/tree/v0.1"),
                         ["JarbasSkills", "skill-wolfie"])

        url = "https://github.com/MycroftAI/skill-hello-world"
        self.assertEqual(author_repo_from_github_url(url + "/tree/20.08"),
                         ["MycroftAI", "skill-hello-world"])

        url = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie"
        self.assertEqual(author_repo_from_github_url(url),
                         ["JarbasSkills", "skill-wolfie"])

    def test_skill_name_from_url(self):
        url = "https://github.com/JarbasSkills/skill-wolfie"
        self.assertEqual(skill_name_from_github_url(url), "Wolfie Skill")
        self.assertEqual(skill_name_from_github_url(url + "/tree/v0.1"),
                         "Wolfie Skill")

        url = "https://github.com/MycroftAI/skill-hello-world"
        self.assertEqual(skill_name_from_github_url(url + "/tree/20.08"),
                         "Hello World Skill")

        url = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie"
        self.assertEqual(skill_name_from_github_url(url),
                         "Wolfie Skill")

    def test_dl_url(self):
        # raw
        dl = "https://raw.githubusercontent.com/JarbasSkills/skill-ddg/master/__init__.py"
        self.assertEqual(download_url_from_github_url(dl), dl)

        # blob2raw
        url = "https://github.com/JarbasSkills/skill-ddg/blob/master/__init__.py"
        dl = "https://raw.githubusercontent.com/JarbasSkills/skill-ddg/master/__init__.py"
        self.assertEqual(download_url_from_github_url(url), dl)
        self.assertEqual(blob2raw(url), dl)

        # repo
        url = "https://github.com/JarbasSkills/skill-ddg"
        dl = "https://github.com/JarbasSkills/skill-ddg/archive/master.zip"
        branch = "master"
        self.assertEqual(download_url_from_github_url(url, branch=branch), dl)
        dl = "https://github.com/JarbasSkills/skill-ddg/archive/v0.1.0.zip"
        branch = "v0.1.0"
        self.assertEqual(download_url_from_github_url(url, branch=branch), dl)


# NOTE bellow make actual http requests
class TestGithubUrlValidation(unittest.TestCase):

    def test_branch(self):
        url = "https://github.com/JarbasSkills/skill-ddg"
        self.assertEqual(validate_branch("master", url), True)
        self.assertEqual(validate_branch("V666", url), False)

        # bad url
        self.assertRaises(
            GithubInvalidUrl, validate_branch, "master", "BAD URL"
        )

    def test_skill(self):
        # explicit branch
        url = "https://github.com/JarbasSkills/skill-ddg"
        branch = "master"
        self.assertTrue(validate_github_skill_url(url, branch))
        self.assertEqual(is_valid_github_skill_url(url, branch), True)

        # unknown branch
        self.assertEqual(is_valid_github_skill_url(url), False)
        self.assertRaises(
            GithubInvalidUrl, validate_github_skill_url, url
        )

        # implicit branch
        url = "https://github.com/JarbasSkills/skill-ddg/tree/v0.1.0"
        self.assertTrue(validate_github_skill_url(url))
        self.assertEqual(is_valid_github_skill_url(url), True)

        # non existing branch
        url = "https://github.com/JarbasSkills/skill-ddg/tree/vEvil666"
        self.assertRaises(
            GithubNotSkill, validate_github_skill_url, url
        )
        self.assertEqual(is_valid_github_skill_url(url), False)

        # not a skill repo
        url = "https://github.com/MycroftAI/lingua-franca/tree/master"
        self.assertRaises(
            GithubNotSkill, validate_github_skill_url, url
        )
        self.assertEqual(is_valid_github_skill_url(url), False)

    def test_templates(self):
        # unknown branch
        url = "https://github.com/JarbasSkills/skill-ddg"
        template = GithubUrls.SKILL
        self.assertRaises(
            GithubInvalidBranch, match_url_template, url, template
        )

        # explicit branch
        branch = "v0.1.0"
        match = "https://raw.githubusercontent.com/JarbasSkills/skill-ddg/v0.1.0/__init__.py"
        self.assertEqual(match_url_template(url, template, branch), match)

        template = GithubUrls.README
        match = "https://raw.githubusercontent.com/JarbasSkills/skill-ddg/v0.1.0/README.md"
        self.assertEqual(match_url_template(url, template, branch), match)

        template = GithubUrls.LICENSE
        match = "https://raw.githubusercontent.com/JarbasSkills/skill-ddg/v0.1.0/LICENSE"
        self.assertEqual(match_url_template(url, template, branch), match)

        # implicit branch
        url = "https://github.com/JarbasSkills/skill-wolfie/tree/v0.1"

        template = GithubUrls.REQUIREMENTS
        match = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie/v0.1/requirements.txt"
        self.assertEqual(match_url_template(url, template), match)

        template = GithubUrls.DOWNLOAD
        match = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie/archive/v0.1.zip"
        self.assertEqual(match_url_template(url, template), match)

        template = GithubUrls.DOWNLOAD_TARBALL
        match = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie/archive/v0.1.tar.gz"
        self.assertEqual(match_url_template(url, template), match)

        # TODO manifest, skill_requirements, desktop, icon, skill_json
