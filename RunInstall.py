"""
TheNexusAvenger

Runs the install.
"""

from helper.Path import pathFileExists
from helper.InstallContext import InstallContext
from software.Applications import presets
from software.ArchSetup import setUpArch


# Set up the specifics for the operating system.
if pathFileExists("pacman"):
    setUpArch()

# Run the install.
context = InstallContext()
for installFunction in presets:
    installFunction(context)
context.updatePackages()
context.installQueuedPackages()