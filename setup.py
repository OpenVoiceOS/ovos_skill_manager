from setuptools import setup

def _get_version():
    with open('ovos_skills_manager/versioning/osm_versions.py') as versions:
        for line in versions:
            if line.startswith('CURRENT_OSM_VERSION'):
                # CURRENT_OSM_VERSION = "0.0.10a9" --> "0.0.10a9"
                return line.replace('"','').strip('\n').split('= ')[1]

setup(
    name='ovos-skills-manager',
    packages=['ovos_skills_manager',
              'ovos_skills_manager.github',
              'ovos_skills_manager.appstores',
              'ovos_skills_manager.scripts',
              'ovos_skills_manager.versioning',
              'ovos_skills_manager.local_skill'],
    url='https://github.com/OpenVoiceOS/ovos_skill_manager',
    license='Apache-2.0',
    author='JarbasAI',
    install_requires=["packaging",
                      "ovos_skill_installer>=0.0.5",
                      "json_database~=0.7",
                      "combo-lock~=0.2",
                      "requests",
                      "requests-cache",
                      "ovos_utils~=0.0.15",
                      "pako>=0.2.3",
                      "PyYaml",
                      "bs4",
                      "click",
                      "click-default-group>=1.2.2"],
    include_package_data=True,
    author_email='jarbasai@mailfence.com',
    description='Open Voice OS skill manager',
    entry_points='''
        [console_scripts]
        osm=ovos_skills_manager.commands:osm_commands
    ''',
    version=_get_version(),
)
