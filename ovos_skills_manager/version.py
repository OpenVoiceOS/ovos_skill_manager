# The following lines are replaced during the release process.
# START_VERSION_BLOCK
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 13
VERSION_ALPHA = 4
# END_VERSION_BLOCK

CURRENT_OSM_VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_BUILD}"
if VERSION_ALPHA > 0:
    CURRENT_OSM_VERSION += f"a{VERSION_ALPHA}"
