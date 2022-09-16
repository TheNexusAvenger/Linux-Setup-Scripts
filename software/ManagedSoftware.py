"""
TheNexusAvenger

Helper for managing installs that are distro-specific.
"""

import os
from typing import Callable
from helper.InstallContext import InstallContext
from helper.Http import httpGet
from helper.Path import pathFileExists
from helper.Ubuntu import getPpaRepositories, addPpaRepository, installDebFile
from software.PackageManager import getPackageManager


class ManagedSoftware:
    def __init__(self):
        """Creates the managed software helper.
        """

        self.packages = {}
        self.debFiles = []
        self.aptKeys = []
        self.aptRepositories = []
        self.ppaRepositories = []
        self.steps = []


    def addAptKey(self, name: str, url: str) -> "ManagedSoftware":
        """Adds a key for Apt repositories.

        :param name: Name of the key.
        :param url: URL to download the key from.
        :return: The managed software object to allow chaining.
        """

        self.aptKeys.append({
            "name": name,
            "url": url,
        })
        return self


    def addAptRepository(self, name: str, repository: str) -> "ManagedSoftware":
        """Adds an Apt repository.

        :param name: Name of the list file.
        :param repository: Repository to add.
        :return: The managed software object to allow chaining.
        """

        self.aptRepositories.append({
            "name": name,
            "repository": repository,
        })
        return self


    def addDebFile(self, package: str, url: str) -> "ManagedSoftware":
        """Adds a Debian file to download if a package isn't installed.

        :param package: The package to check for before downloading the deb file.
        :param url: URL of the deb file to download.
        :return: The managed software object to allow chaining.
        """

        self.debFiles.append({
            "package": package,
            "url": url,
        })
        return self


    def addPpaRepository(self, repository: str) -> "ManagedSoftware":
        """Adds a PPA repository.

        :param repository: PPA repository to add.
        :return: The managed software object to allow chaining.
        """

        self.ppaRepositories.append(repository)
        return self


    def addPackage(self, packageManager: str, package: str) -> "ManagedSoftware":
        """Adds a package to install.

        :param packageManager: Package manager to install with if it exists.
        :param package: Package to install with the package manager.
        :return: The managed software object to allow chaining.
        """

        if packageManager == "aur":
            packageManager = "yay"
        if packageManager not in self.packages.keys():
            self.packages[packageManager] = []
        self.packages[packageManager].append(package)
        return self


    def addCommonPackage(self, package: str) -> "ManagedSoftware":
        """Adds a package to install that applies to all native package managers.

        :param package: Package to install with the package manager.
        :return: The managed software object to allow chaining.
        """

        self.addPackage("apt", package)
        self.addPackage("pacman", package)
        return self


    def addStep(self, step: Callable[[InstallContext], None]) -> "ManagedSoftware":
        """Adds a step to run.

        :param step: Step to add.
        :return: The managed software object to allow chaining.
        """

        self.steps.append(step)
        return self


    def install(self, context: InstallContext) -> None:
        """Runs the install.

        :param context: Install context for managing the install.
        """

        # Add the PPA repositories.
        if pathFileExists("add-apt-repository"):
            for ppaRepository in self.ppaRepositories:
                if ppaRepository not in getPpaRepositories():
                    addPpaRepository(ppaRepository)

        # Add the apt keys.
        if pathFileExists("apt"):
            for key in self.aptKeys:
                keyPath = "/usr/share/keyrings/" + key["name"]
                if not os.path.exists(keyPath):
                    with open(keyPath, "wb") as file:
                        file.write(httpGet(key["url"]))

        # Add the apt repositories.
        if pathFileExists("apt"):
            for repository in self.aptRepositories:
                repositoryPath = "/etc/apt/sources.list.d/" + repository["name"]
                if not os.path.exists(repositoryPath):
                    repositoryContents = repository["repository"]
                    if repositoryContents.startswith("http"):
                        repositoryContents = httpGet(repositoryContents).decode("utf8")
                    with open(repositoryPath, "w") as file:
                        file.write(repositoryContents)

        # Install the deb files.
        if pathFileExists("dpkg") and pathFileExists("apt"):
            for debFileData in self.debFiles:
                if not getPackageManager("apt").isPackageInstalled(debFileData["package"]):
                    installDebFile(debFileData["url"])

        # Run the step.
        for step in self.steps:
            step(context)

        # Queue the packages.
        for packageManager in self.packages.keys():
            if pathFileExists(packageManager):
                for package in self.packages[packageManager]:
                    context.queuePackage(packageManager, package)