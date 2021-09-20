from collections import OrderedDict
from enum import Enum
from os import path, remove
from packaging import version
from pkg_resources import get_distribution

from click import echo
from json_database import JsonConfigXDG, JsonStorageXDG
from osm import locate_config_file

CURRENT_OSM_VERSION = "0.0.10a5"

def do_launch_version_checks():
    config = locate_config_file()
    if config: # does the config file exist?
        if not check_current_version(config): # does it reflect the most recent version?
            upgrade, config = check_upgrade(config) # if not, do the upgrade routine
            if upgrade:
                config = find_and_perform_osm_upgrades(config)
            # now that we've applied all updates, bump config version to current
            config["version"] = CURRENT_OSM_VERSION
            config.store()
            echo(f"OSM is now v{CURRENT_OSM_VERSION}")

def check_current_version(config:dict=None) -> bool:
    config = config or locate_config_file()
    return version.parse((config.get("version") or "0.0.9")) == version.parse(CURRENT_OSM_VERSION)

def check_upgrade(config:dict=None) -> (bool, dict):
    config = config or locate_config_file()
    # find the last upgrade path that was performed
    last_upgrade = config.get('last_upgrade')
    if not last_upgrade:
        config['last_upgrade'] = 'v0.0.9a5' # 0.0.9 -> 0.0.10 is first-ever upgrade with code
        config.store()
        return True, config # We haven't done the 0.0.10 upgrade yet, so... yeah

    last_upgrade = version.parse(last_upgrade) # cast the version to something we can compare
    upgrade_versions = list(UPGRADE_PATHS.keys())
    if last_upgrade == upgrade_versions[-1]:
            return False, config  # we have done the most recent possible upgrade
    for upgrade_version in upgrade_versions:
        if last_upgrade < upgrade_version:
            return True, config

def find_and_perform_osm_upgrades(config: dict) -> dict:
    last_upgrade = version.parse(config.get('last_upgrade'))
    for upgrade_version, upgrade_path in UPGRADE_PATHS.items():
        if upgrade_version > last_upgrade:
            upgrade_string = str(upgrade_version)

            config = upgrade_path(config) # upgrade routines should accept and then return config, in case it moves

            config["last_upgrade"] = upgrade_string
            config["version"] = upgrade_string
            config.store()
            echo(f"Upgraded OSM to v{upgrade_string}")
    echo("All OSM updates applied. ", nl=False)
    return config

def upgrade_0_0_10a3(config:JsonStorageXDG=None):
    # Migrate config file
    old_config = config or JsonStorageXDG("OVOS-SkillsManager")
    if path.exists(old_config.path):
        new_config = \
            JsonConfigXDG("OVOS-SkillsManager",
                            subfolder="OpenVoiceOS").merge(old_config,
                                                    skip_empty=False)
        new_config.store()
        remove(old_config.path)
        return new_config
    raise FileNotFoundError("Unable to execute OSM upgrade 0.0.9 --> 0.0.10a3: could not find old config")


UPGRADE_PATHS = OrderedDict({
    # Each version with an upgrade should map to a function, which should accept and return config
    version.parse("0.0.10a3"): upgrade_0_0_10a3
})
