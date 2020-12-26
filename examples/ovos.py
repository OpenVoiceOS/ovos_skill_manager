from ovos_skills_manager.osm import OVOSSkillsManager

ovos = OVOSSkillsManager()
ovos.enable_appstore("andlo")

print(ovos.total_skills)
for s in ovos.appstores:
    print(s)

for s in ovos:
    print(s.skill_name)

exit()
ovos.enable_appstore("pling")
for s in ovos.search_skills("voip"):
    print(s.as_json)

exit()
ovos.enable_appstore("andlo")

for s in ovos.search_skills("jarbas"):
    print(s.skill_name)



