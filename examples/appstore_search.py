from ovos_skills_manager import MycroftMarketplace

appstore = MycroftMarketplace()

url = "https://github.com/richhowley/national-parks-skill"
res = appstore.search_skills_by_url(url, as_json=True)
assert res[0]["url"] == url

res = appstore.search_skills_by_name("laugh", as_json=True)
assert res[0]['url'] == "https://github.com/JarbasSkills/skill-laugh"


res = appstore.search_skills_by_description("duck duck go", as_json=True)
assert res[0]['foldername'] == 'fallback-duckduckgo'

res = appstore.search_skills_by_author("mycroft", as_json=True)
for s in res:
    assert s['authorname'] == "MycroftAI"

res = appstore.search_skills_by_tag("query", as_json=True)
print(len(res))


res = appstore.search_skills_by_category("information", as_json=True)
print(len(res))


res = appstore.search_skills_by_author("jarbas", as_json=True, thresh=0.65)
assert res[0]['authorname'] == "JarbasSkills"
