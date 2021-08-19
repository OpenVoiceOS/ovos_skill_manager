from ovos_skills_manager.commands import osm_commands
from ovos_skills_manager.scripts import upgrade_osm

if __name__ == '__main__':
    upgrade, _conf = upgrade_osm.check_upgrade()
    if upgrade:
        print("Performing OSM upgrades.")
        upgrade_osm.find_and_perform_osm_upgrades(_conf)
    osm_commands()