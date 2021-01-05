from ovos_skills_manager.osm import OVOSSkillsManager

ovos = OVOSSkillsManager()

print(ovos.total_skills)
for s in ovos.appstores:
    print(s)

for s in ovos:
    print(s.skill_name)


ovos.enable_appstore("pling")
for s in ovos.search_skills("voip"):
    print(s.json)


ovos.enable_appstore("andlo")

for s in ovos.search_skills("jarbas"):
    print(s.skill_name)



