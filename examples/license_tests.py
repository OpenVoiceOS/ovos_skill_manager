from ovos_skills_manager.github import get_license_type_from_github_url

agpls = ["https://github.com/skeledrew/brain-skill",
         "https://github.com/danielquinn/mycroft-evil-laugh",
         "https://github.com/Quinn2017/Skill-Arbitrator-of-Disputes"]
lgpls = [
    "https://github.com/MycroftAI/skill-homeassistant",
    "https://github.com/BongoEADGC6/mycroft-home-assistant",
    "https://github.com/deevrek/homeassistant-skill",
    "https://github.com/00tiagopolicarpo00/skill-radio-rne",
    "https://github.com/chris-mcawesome12/Mycroft-Home-Assistant",
    "https://github.com/mschot/mycroft-smartthings",
    "https://github.com/SomePati/skill-radio-oe1"
]
gpls = [
    "https://github.com/zelmon64/skill-finished-booting",
    "https://github.com/forslund/skill-cocktail",
    "https://github.com/AIIX/plasma-activities-skill",
    "https://github.com/Arc676/Number-Guess-Mycroft-Skill",
    "https://github.com/Arc676/Crystal-Ball-Mycroft-Skill",
    "https://github.com/andlo/picroft-google-aiy-voicekit-skill",
    "https://github.com/danielwine/wikiquote-skill"
]
gpl2 = ["https://github.com/the7erm/mycroft-skill-jupiter-broadcasting",
        "https://github.com/the7erm/mycroft-skill-diagnostics",
        "https://github.com/the7erm/mycroft-skill-podcast",
        "https://github.com/techstoa/mycroft-sonos",
        "https://github.com/the7erm/mycroft-skill-simple-media-controls"]

mits = ["https://github.com/ChanceNCounter/dismissal-skill"]
apaches = ["https://github.com/MycroftAI/fallback-unknown",
           "https://github.com/MycroftAI/fallback-duckduckgo",
           "https://github.com/LinusS1/fallback-recommendations-skill"]

unlicense = ["https://github.com/dmp1ce/mycroft-bitcoinprice-skill",
             "https://github.com/Gits3/Lottery-Skill",
             "https://github.com/sofwerx/mycroft-articlekeyword-skill",
             "https://github.com/mason88/skill-federal-closings"]

epl2 = ["https://github.com/openhab/openhab-mycroft"]
epl1 = ["https://github.com/mortommy/mycroft-skill-openhab"]


isc = ["https://github.com/k3yb0ardn1nja/mycroft-skill-kodi",
        "https://github.com/kfarwell/mycroft-skill-quodlibet"]

# these are missing the MIT header and regular detection will fail
mit_fails = ["https://github.com/MatthewScholefield/skill-question-learner",
             "https://github.com/ITE-5th/skill-face-recognizer",
             "https://github.com/MatthewScholefield/skill-kickstarter-tracker",
             "https://github.com/jaller94/skill-rock-paper-scissors",
             "https://github.com/JamesPoole/podcast-skill",
             "https://github.com/MatthewScholefield/skill-repeat-recent",
             "https://github.com/avimeens/skill-wemo-controller-using-wit",
             "https://github.com/mathias/skill-heroku-status",
             "https://github.com/JamesPoole/skill-tuner"]

# not the full license, but links to it
apache_fails = ["https://github.com/camuthig/mycroft-lifx"]


for url in mits + mit_fails:
    assert get_license_type_from_github_url(url, "master") == "mit"

for url in isc:
    assert get_license_type_from_github_url(url, "master") == "isc"

for url in apaches + apache_fails:
    assert get_license_type_from_github_url(url, "master") == "apache-2.0"

for url in epl1:
    assert get_license_type_from_github_url(url, "master") == "epl-1.0"

for url in epl2:
    assert get_license_type_from_github_url(url, "master") == "epl-2.0"

for url in unlicense:
    assert get_license_type_from_github_url(url, "master") == "unlicense"

for url in gpl2:
    assert get_license_type_from_github_url(url, "master") == "gpl-2.0"

for url in gpls:
    assert get_license_type_from_github_url(url, "master") == "gpl-3.0"


for url in agpls:
    assert get_license_type_from_github_url(url, "master") == "agpl-3.0"

for url in lgpls:
    assert get_license_type_from_github_url(url, "master") == "lgpl-3.0"



