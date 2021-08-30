from setuptools import setup

setup(
    name='ovos-skills-manager',
    version='0.0.9a4',
    packages=['ovos_skills_manager',
              'ovos_skills_manager.github',
              'ovos_skills_manager.appstores',
              'ovos_skills_manager.scripts'],
    url='https://github.com/OpenVoiceOS/ovos_skill_manager',
    license='Apache-2.0',
    author='JarbasAI',
    install_requires=["ovos_skill_installer>=0.0.5",
                      "json_database>=0.5.1",
                      "requests",
                      "requests-cache",
                      "ovos_utils>=0.0.7",
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
)
