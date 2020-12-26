from ovos_skills_manager import SkillEntry
import time

# from github url + implicit branch with json available
url = "https://github.com/MycroftAI/skill-hello-world/tree/20.08"
start = time.time()
s = SkillEntry.from_github_url(url)
end = time.time()
print("took", end - start, "seconds")

# testing requests cache
start = time.time()
s = SkillEntry.from_github_url(url)
end = time.time()
print("took", end - start, "seconds")
