from setuptools import setup

setup(
    name='ovos-skills-manager',
    version='0.0.2',
    packages=['ovos_skills_manager',
              'ovos_skills_manager.github',
              'ovos_skills_manager.appstores',
              'ovos_skills_manager.scripts'],
    url='https://github.com/OpenVoiceOS/ovos_skill_manager',
    license='Apache-2.0',
    author='JarbasAI',
    install_requires=["ovos_skill_installer",
                      "json_database>=0.5.1",
                      "requests",
                      "requests-cache",
                      "ovos_utils>=0.0.4",
                      "pako>=0.2.3",
                      "PyYaml",
                      "bs4",
                      "click"],
    include_package_data=True,
    author_email='jarbasai@mailfence.com',
    description='Open Voice OS skill manager',
    entry_points='''
        [console_scripts]
        osm-sync=ovos_skills_manager.scripts.sync:sync
        osm-search=ovos_skills_manager.scripts.search:search
        osm-install=ovos_skills_manager.scripts.install:install
        osm-enable=ovos_skills_manager.scripts.enable:enable
        osm-disable=ovos_skills_manager.scripts.disable:disable
        osm-priority=ovos_skills_manager.scripts.priority:priority
        osm-print=ovos_skills_manager.scripts.config_print:print_config
        osm-auth=ovos_skills_manager.scripts.add_auth:add_auth
    ''',
)
