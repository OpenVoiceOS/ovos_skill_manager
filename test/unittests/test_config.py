import os
from shutil import copy2

import pytest

MOCKED_VARS = { 'XDG_CACHE_HOME': '/tmp/xdg-cache/',
                'XDG_CONFIG_HOME': '/tmp/xdg-config/',
                'XDG_DATA_HOME': '/tmp/xdg-data/'
                }

def test_mock_envvars():
    for var, val in MOCKED_VARS.items():
        assert os.environ[var] == val

def test_locate_config():
    from ovos_skills_manager.config import _existing_osm_config
    with _existing_osm_config() as config:
        assert config.path == os.environ['XDG_CONFIG_HOME'] + 'OpenVoiceOS/OVOS-SkillsManager.json'

def test_get_config():
   from ovos_skills_manager.config import get_config_object
   with get_config_object() as config:
        assert config

def test_upgrade_migrates_config():
    if os.environ['XDG_CACHE_HOME'] != MOCKED_VARS['XDG_CACHE_HOME']:
        raise EnvironmentError

    from ovos_skills_manager.config import get_config_object
    _path = ''
    with get_config_object() as config:
        assert config
        # set the config to reflect an old version
        config['version'] = '0.0.9'
        config['last_upgrade'] = '0.0.9'
        config.store()
        _path = config.path

    # move the config file to the old location
    old_loc = os.environ['XDG_CACHE_HOME'] + 'json_database/'
    try:
        os.mkdir(old_loc) # ensure the directory exists
    except FileExistsError:
        pass
    copy2(_path, f'{old_loc}/OVOS-SkillsManager.json')
    os.remove(_path)

    from ovos_skills_manager.upgrade_osm import do_launch_version_checks
    from ovos_skills_manager.version import CURRENT_OSM_VERSION
    do_launch_version_checks()
    with get_config_object() as config:
        assert config
        assert config['version'] == CURRENT_OSM_VERSION
