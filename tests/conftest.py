import pytest
from os import environ, path, remove, mkdir

from ovos_skills_manager.osm import OVOSSkillsManager

MOCKED_VARS = { 'XDG_CACHE_HOME': '/tmp/xdg-cache/',
                'XDG_CONFIG_HOME': '/tmp/xdg-config/',
                'XDG_DATA_HOME': '/tmp/xdg-data/'
                }

@pytest.fixture(autouse=True, scope='session')
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch
    monkey = MonkeyPatch()
    yield monkey
    monkey.undo()

@pytest.fixture(autouse=True, scope='session')
def osm_test(monkeymodule):
    """Ensures that OSM tests use mocked XDG environment variables.
    """
    for var, val in MOCKED_VARS.items():
        monkeymodule.setenv(var, val)
        if not path.exists(val):
            mkdir(val)
    print("Set envvars")
    import xdg
    # yield
    # print(xdg.BaseDirectory.xdg_config_home)
    # print("Done")