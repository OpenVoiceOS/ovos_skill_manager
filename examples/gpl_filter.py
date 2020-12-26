from ovos_skills_manager import MycroftMarketplace

appstore = MycroftMarketplace()

for s in appstore.search_skills_by_tag("viral-license"):
    print(s.url, "is viral! License", s.license)


for s in appstore.search_skills_by_tag("permissive-license"):
    print(s.url, "is permissive, it is a good skill! License", s.license)


for s in appstore.search_skills_by_tag("no-license"):
    print(s.url, "does not have a license!! avoid it!!")