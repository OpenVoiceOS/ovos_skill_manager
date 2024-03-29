import os
import sys
import unittest


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "andlo", "default", "all"]

class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from ovos_skills_manager.appstores.ovos import OVOSstore
        OVOSstore().sync_skills_list()

        if os.environ.get("GITHUB_TOKEN"):
            from ovos_skills_manager.session import set_github_token
            set_github_token(os.environ.get("GITHUB_TOKEN"))

    def test_get_skills_mycroft(self):
        from ovos_skills_manager.appstores.mycroft_marketplace import get_mycroft_marketplace_skills
        skills = get_mycroft_marketplace_skills()
        self.assertTrue(any(skills))

    def test_get_skills_ovos(self):
        from ovos_skills_manager.appstores.ovos import get_ovos_skills
        skills = get_ovos_skills()
        self.assertTrue(any(skills))

    # TODO: get_neon needs auth, use env var + GH secret DM

    def test_search_mycroft_all(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "dismissal"
        fuzzy = True
        thresh = 80
        results = search_skill(method="all", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="mycroft")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_mycroft_name(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "dismiss"
        fuzzy = True
        thresh = 80
        results = search_skill(method="name", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="mycroft")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_mycroft_url(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "https://github.com/ChanceNCounter/dismissal-skill"
        fuzzy = False
        thresh = 80
        results = search_skill(method="url", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="mycroft")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_neon_all(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "caffeine"
        fuzzy = True
        thresh = 80
        results = search_skill(method="all", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="neon")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_neon_name(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "Caffeine Wiz"
        fuzzy = True
        thresh = 80
        results = search_skill(method="name", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="neon")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_neon_url(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "https://github.com/NeonGeckoCom/caffeinewiz.neon"
        fuzzy = False
        thresh = 80
        results = search_skill(method="url", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="neon")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_ovos_all(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "launcher"
        fuzzy = True
        thresh = 80
        results = search_skill(method="all", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="ovos")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_ovos_name(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "launcher"
        fuzzy = True
        thresh = 80
        results = search_skill(method="name", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="ovos")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

    def test_search_ovos_url(self):
        from ovos_skills_manager.scripts.search import search_skill
        # methods = ['all', 'name', 'url', 'category', 'author', 'tag', 'description']
        query = "https://github.com/NeonGeckoCom/launcher.neon"
        fuzzy = False
        thresh = 80
        results = search_skill(method="url", query=query, fuzzy=fuzzy, no_ignore_case=False,
                               thresh=thresh, appstore="ovos")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

# TODO: Pling, andlo searches


if __name__ == '__main__':
    unittest.main()
