from ovos_skills_manager import SkillEntry

skills_folder = "installed_skills"

# skill requirements, branch not specified  c
url = "https://github.com/JarbasSkills/mycroft-node-red"
s = SkillEntry.from_github_url(url, "master")
updated = s.install(skills_folder)
print("skill updated:", updated)

# from github url + implicit branch with json available
url = "https://github.com/MycroftAI/skill-hello-world/tree/20.08"
s = SkillEntry.from_github_url(url)
updated = s.install(skills_folder)
print("skill updated:", updated)

updated = s.update(skills_folder)
print("skill updated:", updated)

# test requirements.txt
url = "https://github.com/JarbasSkills/skill-wolfie"
s = SkillEntry.from_github_url(url)
updated = s.install(skills_folder)
print("skill updated:", updated)

# test manifest.yml
# NOTE most likely baresip install will fail because it needs sudo
url = "https://github.com/JarbasSkills/skill-voip"
s = SkillEntry.from_github_url(url)
updated = s.install(skills_folder)
print("skill updated:", updated)
