from click import echo
from ovos_skills_manager import upgrade_osm
from ovos_skills_manager.commands import osm_commands

if __name__ == '__main__':
    upgrade_osm.do_launch_version_checks()
    osm_commands()
