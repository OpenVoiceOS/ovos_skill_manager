Because OSM interacts with XDG-compliant directories, in order to avoid 
altering devs' and testers' config files and skills, we need to mock the
relevant environment variables. In order for this to work, it seems
imports from ovos_skills_manager must take place in the *function* scope.