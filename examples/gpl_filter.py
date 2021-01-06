from ovos_skills_manager import MycroftMarketplace, AndloSkillList

appstore = AndloSkillList()

for s in appstore.search_skills_by_tag("viral-license"):
    # GPL
    # With a strict view on the OpenSource definition, the GPL would be a non-free license.
    # In GPL section 8, it is permitted to add a clause that could restrict the GPL to give it's permission only to specific groups, but this would be in conflict with section 5 of the OpenSource definition.
    # Fortunately, there is no actual software that makes use of GPL section 8, so all currently existing GPLd software is compliant to the OpenSource definition.
    # The GPL prevents code flow from code under GPL into other works being under different even OSI compliant licenses.
    # Note that the GPL still permits collective works and thus allows linking against other independent works as long as this may be achieved by linking unmodified works or only slightly modified works.
    # As the GPL impairs collaboration and as the GPL, does not contain a method to defend against patent suing, the OSSCC does not recommend to use the GPL for new projects.

    # LGPL
    # With a strict view on the OpenSource definition, the LGPL would be a non-free license.
    # In LGPL section 12, it is permitted to add a clause that could restrict the LGPL to give it's permission only to specific groups, but this would be in conflict wth section 5 of the OpenSource definition.
    # Fortunately, there is no actual software that makes use of LGPL section 12, so all currently existing LGPLd software is compliant to the OpenSource definition.

    # The LGPL prevents code flow from code under LGPL into other works being under different OSI compliant licenses.
    # The LGPL however allows to non-LGPL works to link against a LGPL work.
    # As the LGPL does not allow code merging the OSSCC does not recommend to use the LGPL for new projects.
    #
    # Additional note: The applicability of the LGPL's linking exception to interpreted languages like Python is unclear. As of this writing, the issue has not been tested in court.

    # GPLv3
    # The GPLv3 has been published in June 2007. The GPLv3 no longer contains claims that are comparable to section 8 of the GPL, so the GPLv3 is a true OSS license.
    # The GPLv3 added claims to defend against patent suing.
    # Unfortunately, the GPLv3 tries to add further restrictions on collective works and as this is done by using an ambiguous wording,
    # it is expected to create a high risk to distributors for being sued by authors or Copyright holders.
    # As the GPLv3 impairs collaboration even more than the GPL, the OSSCC does not recommend to use the GPLv3 for new projects.

    # CPL
    # The CPL permits only contributions and anhancements to the original work but does not allow to use code from a CPL licensed work in another work.
    # So the CPL is even more restrictive than the GPL.
    # For this reason, the OSSCC does not recommend to use the CPL for new projects.

    # EPL
    # The EPL permits only contributions and anhancements to the original work but does not allow to use code from a EPL licensed work in another work.
    # So the EPL is even more restrictive than the GPL.
    # For this reason, the OSSCC does not recommend to use the EPL for new projects.
    print(s.url, "has a viral license! This might be a problem. License:", s.license)


for s in appstore.search_skills_by_tag("permissive-license"):
    print(s.url, "is permissively licensed! This is good. License:", s.license)


for s in appstore.search_skills_by_tag("no-license"):
    # Some developers think that code with no license is automatically in the public domain.
    # That is not true under today's copyright law; rather, all copyrightable works are copyrighted by default.
    # This includes programs. Absent a license to grant users freedom, they don't have any.
    # In some countries, users that download code with no license may infringe copyright merely by compiling it or running it.
    print(s.url, "does not have a license!! avoid it!!")