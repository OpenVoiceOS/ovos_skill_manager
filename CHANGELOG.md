# Changelog

## [Unreleased](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/HEAD)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/V0.0.11a2...HEAD)

**Implemented enhancements:**

- Handle Commented requirements files [\#94](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/94)

**Fixed bugs:**

- Fix local commented requirements file handling [\#95](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/95) ([NeonDaniel](https://github.com/NeonDaniel))

## [V0.0.11a2](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/V0.0.11a2) (2022-03-15)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/V0.0.11a1...V0.0.11a2)

**Fixed bugs:**

- fix .desktop homescreen message [\#90](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/90) ([JarbasAl](https://github.com/JarbasAl))

## [V0.0.11a1](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/V0.0.11a1) (2022-03-15)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/V0.0.10...V0.0.11a1)

**Fixed bugs:**

- Fix typo in `os.remove` call in AbstractAppstore [\#91](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/91) ([NeonDaniel](https://github.com/NeonDaniel))

## [V0.0.10](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/V0.0.10) (2022-03-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/V0.0.10a1...V0.0.10)

## [V0.0.10a1](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/V0.0.10a1) (2022-03-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/V0.0.10a20...V0.0.10a1)

## [V0.0.10a20](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/V0.0.10a20) (2022-02-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/0.0.9a4...V0.0.10a20)

**Implemented enhancements:**

- Emit a bus event or callback when sync has completed [\#55](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/55)
- Move hardcoded config paths to XDG-compliant directories [\#16](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/16)
- Add logging of skill installation errors in addition to emitting errors [\#88](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/88) ([NeonDaniel](https://github.com/NeonDaniel))
- Spec types for all SkillEntry properties [\#85](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/85) ([NeonDaniel](https://github.com/NeonDaniel))
- Add `SkillEntry.from_directory` [\#81](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/81) ([NeonDaniel](https://github.com/NeonDaniel))
- Add annotations to all Github functions [\#79](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/79) ([NeonDaniel](https://github.com/NeonDaniel))
- add upgrade mechanism; move config file to config folder; bumpver [\#53](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/53) ([ChanceNCounter](https://github.com/ChanceNCounter))
- add type annotations to several files [\#51](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/51) ([ChanceNCounter](https://github.com/ChanceNCounter))

**Fixed bugs:**

- ovos utils 0.0.12 compatibility [\#82](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/82)
- Check on rate limit and pause for it [\#65](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/65)
- Skill ID/folder basename is indeterminate [\#58](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/58)
- Fix dependency bugs [\#86](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/86) ([NeonDaniel](https://github.com/NeonDaniel))
- Troubleshoot ovos-utils version compat. [\#80](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/80) ([NeonDaniel](https://github.com/NeonDaniel))
- Catch and handle missing optional skill files [\#76](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/76) ([NeonDaniel](https://github.com/NeonDaniel))
- fix: osm.versioning missing from setup.py [\#73](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/73) ([ChanceNCounter](https://github.com/ChanceNCounter))
- Fix UUID Parsing [\#69](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/69) ([NeonDaniel](https://github.com/NeonDaniel))
- handle some missing fields  [\#63](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/63) ([JarbasAl](https://github.com/JarbasAl))
- fix SkillEntry.generate\_desktop\_file\(\) ConcatErr [\#60](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/60) ([ChanceNCounter](https://github.com/ChanceNCounter))

**Closed issues:**

- Find a free coverage bot and set it up [\#39](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/39)

**Merged pull requests:**

- feat/workflows [\#89](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/89) ([JarbasAl](https://github.com/JarbasAl))
- Add automation for publishing to PyPI [\#87](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/87) ([NeonDaniel](https://github.com/NeonDaniel))
- add codecov to github workflow [\#75](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/75) ([ChanceNCounter](https://github.com/ChanceNCounter))
- Add action to run workflow on PR to main branch [\#70](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/70) ([NeonDaniel](https://github.com/NeonDaniel))
- moved test repo [\#64](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/64) ([ChanceNCounter](https://github.com/ChanceNCounter))

## [0.0.9a4](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/0.0.9a4) (2021-08-30)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/0.0.6...0.0.9a4)

**Implemented enhancements:**

- add bus event [\#56](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/56) ([JarbasAl](https://github.com/JarbasAl))
- unify deps in setup.py; bump: 0.0.9 dev cycle [\#49](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/49) ([ChanceNCounter](https://github.com/ChanceNCounter))
- Fix skill installation from URL [\#35](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/35) ([NeonDaniel](https://github.com/NeonDaniel))
- Add method to install skill via URL without SkillEntry/Appstore parsing [\#33](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/33) ([NeonDaniel](https://github.com/NeonDaniel))
- Requirements Parsing and Unit Tests [\#27](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/27) ([NeonDaniel](https://github.com/NeonDaniel))
- protect against download\_url hijacking [\#22](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/22) ([JarbasAl](https://github.com/JarbasAl))

**Fixed bugs:**

- Skill installation strips '.' from icon file extension, fails to install skills [\#45](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/45)
- Dependencies for appstore skills with branch specs [\#30](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/30)
- OSM SkillEntry.requirements is list not dict [\#25](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/25)
- appstore.get\_skills\_list: check for \[\] or None return [\#24](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/24)
- fix install from url [\#57](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/57) ([JarbasAl](https://github.com/JarbasAl))
- detect skill folder [\#52](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/52) ([ChanceNCounter](https://github.com/ChanceNCounter))
- fix: typo in created icon name, ensure dir exists [\#46](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/46) ([ChanceNCounter](https://github.com/ChanceNCounter))
- add missing dep: click-default-group [\#36](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/36) ([ChanceNCounter](https://github.com/ChanceNCounter))
- fix sync appstore skill updates [\#32](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/32) ([JarbasAl](https://github.com/JarbasAl))
- detect pling downtime [\#31](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/31) ([JarbasAl](https://github.com/JarbasAl))
- bump OSM version, ref to mycroft-core version [\#29](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/29) ([ChanceNCounter](https://github.com/ChanceNCounter))
- Tempfix skill installation requirements issue [\#26](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/26) ([NeonDaniel](https://github.com/NeonDaniel))

**Merged pull requests:**

- bump: 0.0.8 final [\#48](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/48) ([ChanceNCounter](https://github.com/ChanceNCounter))

## [0.0.6](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/0.0.6) (2021-05-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/0.0.5...0.0.6)

**Implemented enhancements:**

- search\_by\_url with branch [\#21](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/21) ([JarbasAl](https://github.com/JarbasAl))
- neon\_git\_token [\#18](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/18) ([NeonDaniel](https://github.com/NeonDaniel))

**Fixed bugs:**

- OSM Installing from default branch instead of specified one [\#17](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/17)
- osm-search and osm-install invalid osm.appstores references [\#15](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/15)
- better bootstrap control [\#20](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/20) ([JarbasAl](https://github.com/JarbasAl))
- fix \#17 [\#19](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/19) ([ChanceNCounter](https://github.com/ChanceNCounter))

## [0.0.5](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/0.0.5) (2021-05-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/0.0.1...0.0.5)

**Implemented enhancements:**

- Command-line improvements [\#8](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/8)
- \[Idea\] Use osm like another package manager [\#7](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/7)
- \[feature request\] Show repos on osm-search [\#4](https://github.com/OpenVoiceOS/ovos_skill_manager/issues/4)
- refactor: use unified 'osm \<cmd\>', not 'osm-\<cmd\>' [\#14](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/14) ([ChanceNCounter](https://github.com/ChanceNCounter))
- add neon\_license [\#2](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/2) ([JarbasAl](https://github.com/JarbasAl))

**Merged pull requests:**

- add .gitignore \(cp from lingua franca\) [\#13](https://github.com/OpenVoiceOS/ovos_skill_manager/pull/13) ([ChanceNCounter](https://github.com/ChanceNCounter))

## [0.0.1](https://github.com/OpenVoiceOS/ovos_skill_manager/tree/0.0.1) (2021-01-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos_skill_manager/compare/5e35c78dd3c97a892064d5f02cabf6be9b5d812e...0.0.1)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
