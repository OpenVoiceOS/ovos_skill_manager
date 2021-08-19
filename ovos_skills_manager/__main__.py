from ovos_skills_manager import upgrade_osm
from ovos_skills_manager.commands import osm_commands

if __name__ == '__main__':
    upgrade, _conf = upgrade_osm.check_upgrade()
    if upgrade:
        upgrade_osm.find_and_perform_osm_upgrades(_conf)
    osm_commands()
