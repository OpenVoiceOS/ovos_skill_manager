import unittest
from ovos_skills_manager.github import get_license_type
from ovos_skills_manager.licenses import is_permissive, is_viral, parse_license_type


# TODO setup a test skill repo, since a random url can simply vanish


class TestGithubUrlParsing(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        # some examples gathered from parsing andlo's list
        self.agpls = ["https://github.com/skeledrew/brain-skill",
                      "https://github.com/danielquinn/mycroft-evil-laugh",
                      "https://github.com/Quinn2017/Skill-Arbitrator-of-Disputes"]
        self.lgpls = [
            "https://github.com/MycroftAI/skill-homeassistant",
            "https://github.com/BongoEADGC6/mycroft-home-assistant",
            "https://github.com/deevrek/homeassistant-skill",
            "https://github.com/00tiagopolicarpo00/skill-radio-rne",
            "https://github.com/chris-mcawesome12/Mycroft-Home-Assistant",
            "https://github.com/mschot/mycroft-smartthings",
            "https://github.com/SomePati/skill-radio-oe1"
        ]
        self.gpls = [
            "https://github.com/zelmon64/skill-finished-booting",
            "https://github.com/forslund/skill-cocktail",
            "https://github.com/AIIX/plasma-activities-skill",
            "https://github.com/Arc676/Number-Guess-Mycroft-Skill",
            "https://github.com/Arc676/Crystal-Ball-Mycroft-Skill",
            "https://github.com/andlo/picroft-google-aiy-voicekit-skill",
            "https://github.com/danielwine/wikiquote-skill"
        ]
        self.gpl2 = [
            "https://github.com/the7erm/mycroft-skill-jupiter-broadcasting",
            "https://github.com/the7erm/mycroft-skill-diagnostics",
            "https://github.com/the7erm/mycroft-skill-podcast",
            "https://github.com/techstoa/mycroft-sonos",
            "https://github.com/the7erm/mycroft-skill-simple-media-controls"]
        self.mits = ["https://github.com/ChanceNCounter/dismissal-skill"]
        self.apaches = ["https://github.com/MycroftAI/fallback-unknown",
                        "https://github.com/MycroftAI/fallback-duckduckgo",
                        "https://github.com/LinusS1/fallback-recommendations-skill"]
        self.unlicense = [
            "https://github.com/dmp1ce/mycroft-bitcoinprice-skill",
            "https://github.com/Gits3/Lottery-Skill",
            "https://github.com/sofwerx/mycroft-articlekeyword-skill",
            "https://github.com/mason88/skill-federal-closings"]
        self.epl2 = ["https://github.com/openhab/openhab-mycroft"]
        self.epl1 = ["https://github.com/mortommy/mycroft-skill-openhab"]
        self.isc = ["https://github.com/k3yb0ardn1nja/mycroft-skill-kodi",
                    "https://github.com/kfarwell/mycroft-skill-quodlibet"]
        # these are missing the MIT header and regular detection will fail
        self.mit_fails = [
            "https://github.com/MatthewScholefield/skill-question-learner",
            "https://github.com/ITE-5th/skill-face-recognizer",
            "https://github.com/MatthewScholefield/skill-kickstarter-tracker",
            "https://github.com/jaller94/skill-rock-paper-scissors",
            "https://github.com/JamesPoole/podcast-skill",
            "https://github.com/MatthewScholefield/skill-repeat-recent",
            "https://github.com/avimeens/skill-wemo-controller-using-wit",
            "https://github.com/mathias/skill-heroku-status",
            "https://github.com/JamesPoole/skill-tuner"]
        # not the full license, but links to it
        self.apache_fails = ["https://github.com/camuthig/mycroft-lifx"]

        # TODO more license text examples
        self.bsd0_template = """Permission to use, copy, modify, and distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
        THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
        """
        self.isc_template = """Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
        THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
        """
        self.mit_template_noheader = """
        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
        The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """

    def test_parse(self):
        self.assertEqual(parse_license_type(self.mit_template_noheader), "mit")
        self.assertEqual(parse_license_type(self.isc_template), "isc")
        self.assertEqual(parse_license_type(self.bsd0_template), "0bsd")

    def test_detect_viral(self):
        for lic in [self.mit_template_noheader, self.isc_template,
                    self.bsd0_template]:
            lic = parse_license_type(lic)
            self.assertFalse(is_viral(lic))
            self.assertTrue(is_permissive(lic))

        for url in self.apaches + self.apache_fails + self.mits + \
                   self.mit_fails + self.isc + self.unlicense:
            # TODO license text examples, not url
            lic = get_license_type(url, "master")
            self.assertFalse(is_viral(lic))
            self.assertTrue(is_permissive(lic))

        for url in self.agpls + self.lgpls + self.gpls + self.gpl2 + \
                   self.epl1 + self.epl2:
            # TODO license text examples, not url
            lic = get_license_type(url, "master")
            self.assertTrue(is_viral(lic))
            self.assertFalse(is_permissive(lic))

    def test_detect_type_from_url(self):
        for url in self.mits + self.mit_fails:
            self.assertEqual(get_license_type(url, "master"), "mit")
        for url in self.isc:
            self.assertEqual(get_license_type(url, "master"), "isc")
        for url in self.apaches + self.apache_fails:
            self.assertEqual(get_license_type(url, "master"), "apache-2.0")
        for url in self.epl1:
            self.assertEqual(get_license_type(url, "master"), "epl-1.0")
        for url in self.epl2:
            self.assertEqual(get_license_type(url, "master"), "epl-2.0")
        for url in self.unlicense:
            self.assertEqual(get_license_type(url, "master"), "unlicense")
        for url in self.gpl2:
            self.assertEqual(get_license_type(url, "master"), "gpl-2.0")
        for url in self.gpls:
            self.assertEqual(get_license_type(url, "master"), "gpl-3.0")
        for url in self.agpls:
            self.assertEqual(get_license_type(url, "master"), "agpl-3.0")
        for url in self.lgpls:
            self.assertEqual(get_license_type(url, "master"), "lgpl-3.0")
