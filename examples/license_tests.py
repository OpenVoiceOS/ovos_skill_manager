from ovos_skills_manager.github import get_license_type_from_github_url

agpls = ["https://github.com/MycroftAI/selene-backend"]
lgpls = [
    "https://github.com/MycroftAI/skill-homeassistant"
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
mits = ["https://github.com/ChanceNCounter/dismissal-skill"]
apaches = ["https://github.com/MycroftAI/fallback-unknown",
           "https://github.com/MycroftAI/fallback-duckduckgo",
           "https://github.com/LinusS1/fallback-recommendations-skill"]

for url in gpls:
    assert get_license_type_from_github_url(url) == "gpl"

for url in agpls:
    assert get_license_type_from_github_url(url) == "agpl"

for url in lgpls:
    assert get_license_type_from_github_url(url) == "lgpl"

for url in mits:
    assert get_license_type_from_github_url(url) == "mit"

for url in apaches:
    assert get_license_type_from_github_url(url) == "apache-2.0"

