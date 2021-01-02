from ovos_skills_manager import SkillEntry

# from github url with json available  (all urls work)
url = "https://github.com/JarbasSkills/skill-wolfie/blob/master/__init__.py"
url = "https://github.com/JarbasSkills/skill-wolfie/blob/v0.1/res/desktop/skill.json"
url = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie/v0.1/res/desktop/skill.json"
url = "https://github.com/JarbasSkills/skill-wolfie"
s = SkillEntry.from_github_url(url)
print(s.json)


# from github url with no .json available
url = "https://github.com/MycroftAI/skill-hello-world"
s = SkillEntry.from_github_url(url)
print(s.json)

# from github url + implicit branch with json available
url = "https://github.com/MycroftAI/skill-hello-world/tree/20.08"
s = SkillEntry.from_github_url(url)
print(s.json)


# parse .json from github url to file (all urls work assuming json in standard location)
url = "https://github.com/JarbasSkills/skill-wolfie/blob/master/__init__.py"
url = "https://github.com/JarbasSkills/skill-wolfie"
url = "https://raw.githubusercontent.com/JarbasSkills/skill-wolfie/v0.1/res/desktop/skill.json"
url = "https://github.com/JarbasSkills/skill-wolfie/blob/v0.1/res/desktop/skill.json"
s = SkillEntry.from_json(url)
print(s.json)

# parse .json from github url to file (json not available)
url = "https://github.com/AIIX/youtube-skill"
s = SkillEntry.from_json(url)
print(s.json)
