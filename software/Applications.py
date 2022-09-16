"""
TheNexusAvenger

Applications to install.
"""

import json
import os
import stat
import tempfile
import zipfile
from helper.Http import httpGet
from helper.InstallContext import InstallContext
from helper.Path import pathFileExists
from helper.Process import runProcess
from software.ManagedSoftware import ManagedSoftware


def setUpGrapejuiceSources(context: InstallContext) -> None:
    """Sets up the sources for Grapejuice.
    """

    if pathFileExists("apt"):
        runProcess(["dpkg", "--add-architecture", "i386"])


def installNexusLULauncher(context: InstallContext) -> None:
    """Installs Nexus LU Launcher.
    """

    # Download Nexus LU Launcher.
    if not os.path.exists("/usr/local/lib/nlul/Nexus-LU-Launcher"):
        # Get the latest tag.
        print("Downloading Nexus LU Launcher")
        latestTag = json.loads(httpGet("https://github.com/TheNexusAvenger/Nexus-LU-Launcher/releases/latest", {"Accept": "application/json"}).decode("utf8"))["tag_name"]

        # Download the archive.
        downloadPath = tempfile.NamedTemporaryFile(suffix=".zip").name
        with open(downloadPath, "wb") as file:
            file.write(httpGet("https://github.com/TheNexusAvenger/Nexus-LU-Launcher/releases/download/" + latestTag + "/Nexus-LU-Launcher-Linux-x64.zip"))

        # Extract the archive.
        nlulArchive = zipfile.ZipFile(downloadPath)
        nlulArchive.extractall("/usr/local/lib/nlul/")

        # Make the client executable.
        print("Extracting Nexus LU Launcher")
        executableLocation = "/usr/local/lib/nlul/Nexus-LU-Launcher"
        executableStat = os.stat(executableLocation)
        os.chmod(executableLocation, executableStat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # Download the icon.
        iconLocation = "/usr/local/lib/nlul/NexusLULauncherLogo.png"
        if not os.path.exists(iconLocation):
            with open(iconLocation, "wb") as file:
                file.write(httpGet("https://raw.githubusercontent.com/TheNexusAvenger/Nexus-LU-Launcher/master/NLUL.GUI/Assets/Images/NexusLegoUniverseLauncherLogo.png"))


def prepareRojo(context: InstallContext) -> None:
    """Installs the Cargo package manager and prepares for Rojo.
    """

    # Install Cargo.
    if not pathFileExists("cargo") and pathFileExists("apt"):
        downloadPath = tempfile.NamedTemporaryFile(suffix=".sh").name
        with open(downloadPath, "wb") as file:
            file.write(httpGet("https://sh.rustup.rs"))
        runProcess(["sh", downloadPath])
        runProcess(["apt", "install", "-y", "pkg-config"])


# Programing Languages
java = ManagedSoftware()\
    .addPpaRepository("ppa:linuxuprising/java")\
    .addPackage("apt", "oracle-java17-installer")\
    .addPackage("aur", "jdk")
dotnet = ManagedSoftware()\
    .addDebFile("dotnet-sdk-6.0", "https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb")\
    .addCommonPackage("dotnet-sdk-6.0")\
    .addPackage("apt", "aspnetcore-runtime-6.0")\
    .addPackage("pacman", "aspnet-runtime-6.0")
pythonPip = ManagedSoftware()\
    .addPackage("apt", "python3-pip")\
    .addPackage("pacman", "python-pip")

# Games
wine = ManagedSoftware()\
    .addAptKey("winehq-archive.key", "https://dl.winehq.org/wine-builds/winehq.key")\
    .addAptRepository("winehq-jammy.sources", "https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources")\
    .addPackage("apt", "wine-stable")\
    .addPackage("pacman", "wine")\
    .addPackage("pacman", "gnutls")\
    .addPackage("pacman", "lib32-gnutls")\
    .addPackage("pacman", "libpulse")\
    .addPackage("pacman", "lib32-libpulse")
grapejuice = ManagedSoftware()\
    .addStep(setUpGrapejuiceSources)\
    .addAptKey("grapejuice-archive-keyring.gpg", "https://gitlab.com/brinkervii/grapejuice/-/raw/master/ci_scripts/signing_keys/public_key.gpg")\
    .addAptRepository("grapejuice.list", "deb [signed-by=/usr/share/keyrings/grapejuice-archive-keyring.gpg] https://brinkervii.gitlab.io/grapejuice/repositories/debian/ universal main")\
    .addPackage("apt", "grapejuice")\
    .addPackage("aur", "grapejuice")
steam = ManagedSoftware()\
    .addPackage("apt", "steam-installer")\
    .addPackage("pacman", "steam")
minecraft = ManagedSoftware()\
    .addDebFile("minecraft-launcher", "https://launcher.mojang.com/download/Minecraft.deb")\
    .addPackage("aur", "minecraft-launcher")
nexusLULauncher = ManagedSoftware()\
    .addStep(installNexusLULauncher)

# Text Editors / Development Environments
vscode = ManagedSoftware()\
    .addDebFile("code", "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64")\
    .addPackage("aur", "visual-studio-code-bin")
vim = ManagedSoftware()\
    .addCommonPackage("vim")
audacity = ManagedSoftware()\
    .addPackage("pacman", "audacity")
    # TODO: Add Ubuntu installer - snap install audacity
# TODO: Fusion 360

# Communication
discord = ManagedSoftware()\
    .addDebFile("discord", "https://discordapp.com/api/download?platform=linux&format=deb")\
    .addPackage("pacman", "discord")
chrome = ManagedSoftware()\
    .addDebFile("google-chrome-stable", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")\
    .addPackage("aur", "google-chrome")

# GUI Utilities
sqliteBrowser = ManagedSoftware()\
    .addCommonPackage("sqlitebrowser")
obs = ManagedSoftware()\
    .addPpaRepository("ppa:obsproject/obs-studio")\
    .addPackage("apt", "ffmpeg")\
    .addPackage("apt", "v4l2loopback-dkms")\
    .addCommonPackage("obs-studio")
openBoard = ManagedSoftware()\
    .addPackage("apt", "openboard")\
    .addPackage("aur", "openboard")
virtualMachineManager = ManagedSoftware()\
    .addCommonPackage("virt-manager")
balenaEtcher = ManagedSoftware()\
    .addAptKey("balena-etcher-archive-keyring.gpg", "https://dl.cloudsmith.io/public/balena/etcher/gpg.70528471AFF9A051.key")\
    .addAptRepository("balena-etcher.list", "https://dl.cloudsmith.io/public/balena/etcher/config.deb.txt?distro=ubuntu&codename=jammy&version=22.04&arch=x86_64")\
    .addPackage("apt", "balena-etcher-electron")\
    .addPackage("aur", "balena-etcher")
gparted = ManagedSoftware()\
    .addCommonPackage("gparted")

# Desktop functionality
wayland = ManagedSoftware()\
    .addPackage("pacman", "plasma-wayland-session")
    # TODO: Add Ubuntu installer
wacomActivePen = ManagedSoftware()\
    .addPackage("pacman", "kcm-wacomtablet")
    # TODO: Add Ubuntu installer

# CLI Utilities
neofetch = ManagedSoftware()\
    .addCommonPackage("neofetch")
git = ManagedSoftware()\
    .addCommonPackage("git")
bashtop = ManagedSoftware()\
    .addCommonPackage("bashtop")
tree = ManagedSoftware()\
    .addCommonPackage("tree")
rojo = ManagedSoftware()\
    .addStep(prepareRojo)\
    .addPackage("pacman", "rustup")
# TODO: Howdy
# TODO: Docker? Podman?

# TODO: AutoHotKey replacement?
# TODO: NVIDIA Broadcast alternative? AMD compatibility?
# TODO: ShareX alternative?

# All presets
presets = {
    java.install,
    dotnet.install,
    pythonPip.install,
    wine.install,
    grapejuice.install,
    steam.install,
    minecraft.install,
    nexusLULauncher.install,
    vscode.install,
    vim.install,
    audacity.install,
    discord.install,
    chrome.install,
    sqliteBrowser.install,
    obs.install,
    openBoard.install,
    virtualMachineManager.install,
    balenaEtcher.install,
    gparted.install,
    wayland.install,
    wacomActivePen.install,
    neofetch.install,
    git.install,
    bashtop.install,
    tree.install,
    rojo.install,
}