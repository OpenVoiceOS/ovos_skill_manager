from collections import OrderedDict
from enum import Enum
from os import path, remove
from packaging import version
from pkg_resources import get_distribution

from click import echo
from json_database import JsonConfigXDG, JsonStorageXDG

def check_upgrade() -> (bool, dict):
    config = JsonConfigXDG("OVOS-SkillsManager", subfolder="OpenVoiceOS")
    if not path.exists(config.path):
        # Check for legacy config
        config = JsonStorageXDG("OVOS-SkillsManager")
        if not path.exists(config.path):
            raise FileNotFoundError("Catastrophic failure: could not locate OSM config. Please contact support.")

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

def find_and_perform_osm_upgrades(config: dict):
    last_upgrade = version.parse(config.get('last_upgrade'))
    for upgrade_version, upgrade_path in UPGRADE_PATHS.items():
        if upgrade_version > last_upgrade:
            upgrade_string = str(upgrade_version)
            if upgrade_path: # it's None or a func, or crash cuz that's bad
                # if it's none, just bump the version in config
                # if it's a func, execute it
                config = upgrade_path(config) # the upgrade routine should accept and then return config
                config["last_upgrade"] = upgrade_string
            config["version"] = upgrade_string
            echo(f"Upgraded OSM to {upgrade_string}")
            config.store()

def upgrade_0_0_10a1(config:JsonStorageXDG=None):
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
    # Versions with no upgrade should map to None, which will simply bump the version # in config
    version.parse("0.0.9a6"): None,
    version.parse("0.0.10a3"): upgrade_0_0_10a1
})
