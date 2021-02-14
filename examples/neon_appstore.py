from ovos_skills_manager.appstores.neon import NeonSkills, AuthenticationError


store = NeonSkills()

try:
    skills = list(store.get_skills_list())
except AuthenticationError:
    # will be read from config if not set
    # store.authenticate("84a0bxxfdf05afxxxxxxxxxxa6fd458xxx6a")
    about = store.search_skills_by_url(
        "https://github.com/NeonGeckoCom/about.neon")[0]
    about.install("my_skills")
    store.clear_authentication()
