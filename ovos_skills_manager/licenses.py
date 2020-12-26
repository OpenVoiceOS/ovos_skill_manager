LICENSE_MATCHERS = {
    "agpl": "GNU AFFERO GENERAL PUBLIC LICENSE",
    "lgpl": "GNU LESSER GENERAL PUBLIC LICENSE",
    "gpl": "GNU GENERAL PUBLIC LICENSE",
    "apache-2.0": "Apache License",
    "unlicense": "https://unlicense.org",
    "mit": "MIT License",
    "mpl-2.0": "Mozilla Public License Version 2.0",
    "bsl-1.0": "Boost Software License - Version 1.0",
    "zlib": "zlib License",
    "afl-3.0": 'Academic Free License ("AFL") v. 3.0',
    "artistic-2.0": "The Artistic License 2.0",
    "bsd-2-clause": "BSD 2-Clause License",
    "bsd-3-clause-clear": "The Clear BSD License",
    "bsd-3-clause": "BSD 3-Clause License",
    "bsd-4-clause": "BSD 4-Clause License",
    "cc-by-4.0": "Creative Commons Attribution 4.0",
    "cc-by-sa-4.0": "Attribution-ShareAlike 4.0 International",
    "cc0-1.0": "CC0 1.0 Universal",
    "cecill-2.1": "CONTRAT DE LICENCE DE LOGICIEL LIBRE CeCILL",
    "ecl-2.0": "Educational Community License",
    "epl-1.0": "Eclipse Public License - v 1.0",
    "epl-2.0": "Eclipse Public License - v 2.0",
    "eupl-1.2": "EUROPEAN UNION PUBLIC LICENCE v. 1.2",
    "eupl-1.1": "Licensed under the EUPL V.1.1",
    "isc": "ISC License",
    "lppl-1.3c": "LPPL Version 1.3c",
    "ms-pl": "Microsoft Public License (Ms-PL)",
    "ms-rl": "Microsoft Reciprocal License (Ms-RL)",
    "ncsa": "University of Illinois/NCSA Open Source License",
    "odbl-1.0": "ODC Open Database License (ODbL)",
    "osl-3.0": 'Open Software License ("OSL") v. 3.0',
    "postgresql": "PostgreSQL License",
    "upl-1.0": "The Universal Permissive License (UPL), Version 1.0",
    "vim": "VIM LICENSE",
    "wtfpl": "DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE"
}


# TODO BSD Zero Clause License, gpl versions, non free licenses
# https://choosealicense.com/licenses/0bsd/


def match_gpls(license):
    pass


def match_bsds(license):
    pass


def match_others(license):
    pass


def get_license_type(license):
    # assumptions
    # - license header is somewhere in the first 10 lines
    # - license list is ordered in a way that first match NEEDS to override others

    # quick and dirty
    header = "\n".join(license.lower().replace(" ", "").split("\n")[:10])
    for k, v in LICENSE_MATCHERS.items():
        if v.lower().replace(" ", "") in header:
            return k
    return license.split("\n")[0].strip()
