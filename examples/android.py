from ovos_skills_manager.github import get_android_json, get_android_url

url = "https://github.com/AIIX/youtube-skill"
print(get_android_url(url, "android-testing"))
print(get_android_json(url, "android-testing"))
