from ovos_skills_manager import SkillEntry

# from github url + implicit branch with json available
url = "https://github.com/MycroftAI/skill-hello-world/tree/20.08"
s = SkillEntry.from_github_url(url)

print(s.generate_readme())

print(s.generate_desktop_file())
