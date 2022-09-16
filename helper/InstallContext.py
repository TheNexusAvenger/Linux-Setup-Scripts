"""
TheNexusAvenger

Helper context for managing installs.
"""

from helper.Process import runProcess
from software.PackageManager import getPackageManager


class InstallContext:
    def __init__(self):
        """Creates the install context.
        """

        self.queuedPackages = {}


    def queuePackage(self, packageManager: str, packageName: str) -> None:
        """Queues a package to be installed.

        :param packageManager: The package manager to install with.
        :param packageName: The package name to install.
        """

        if packageManager not in self.queuedPackages.keys():
            self.queuedPackages[packageManager] = []
        if not getPackageManager(packageManager).isPackageInstalled(packageName) and packageName not in self.queuedPackages[packageManager]:
            self.queuedPackages[packageManager].append(packageName)


    def updatePackages(self) -> None:
        """Updates the packages of the package managers.
        """

        if "apt" in self.queuedPackages.keys():
            runProcess(["apt", "update"])
            runProcess(["apt", "upgrade", "-y"])
        if "pacman" in self.queuedPackages.keys():
            runProcess(["pacman", "--noconfirm", "-Syu"])


    def installQueuedPackages(self) -> None:
        """Installs the queued packages.
        """

        for packageManagerName in self.queuedPackages.keys():
            packages = self.queuedPackages[packageManagerName]
            if len(packages) > 0:
                getPackageManager(packageManagerName).installPackages(packages)
