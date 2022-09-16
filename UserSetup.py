"""
TheNexusAvenger

Sets up the user profile.
"""

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from helper.Http import httpGet
from helper.Path import pathFileExists
from helper.Process import runProcess


# Create the Nexus LU Launcher icon.
localApplicationsDirectory = os.path.expanduser("~/.local/share/applications/")
nlulShortcutLocation = localApplicationsDirectory + "/nexus-lu-launcher.desktop"
if not os.path.exists(localApplicationsDirectory):
    os.makedirs(localApplicationsDirectory)
if not os.path.exists(nlulShortcutLocation):
    print("Creating Nexus LU Launcher desktop icon.")
    with open(nlulShortcutLocation, "w") as file:
        file.write("[Desktop Entry]\r\n")
        file.write("Version=1.0\r\n")
        file.write("Type=Application\r\n")
        file.write("Name=Nexus LU Launcher\r\n")
        file.write("Icon=/usr/local/lib/nlul/NexusLULauncherLogo.png\r\n")
        file.write("Exec=/usr/local/lib/nlul/Nexus-LU-Launcher\r\n")
        file.write("Categories=Game;")

# Install VS Code extensions.
installedVSCodeExtensions = subprocess.check_output(["code", "--list-extensions"]).decode().split("\n")
for extension in ["evaera.vscode-rojo", "Nightrains.robloxlsp", "yzhang.markdown-all-in-one"]:
    if extension not in installedVSCodeExtensions:
        runProcess(["code", "--install-extension", extension])

# Download and run Jetbrains Toolbox.
jetbrainsToolboxInstallLocation = os.path.expanduser("~/.local/share/JetBrains/Toolbox")
if not os.path.exists(jetbrainsToolboxInstallLocation):
    # Download Jetbrains Toolbox.
    print("Downloading Jetbrains Toolbox.")
    jetbrainsToolboxDownloadLocation = tempfile.NamedTemporaryFile(suffix=".tar.gz").name
    with open(jetbrainsToolboxDownloadLocation, "wb") as file:
        file.write(httpGet("https://download.jetbrains.com/toolbox/jetbrains-toolbox-1.25.12627.tar.gz"))

    # Extract Jetbrains Toolbox.
    print("Extracting Jetbrains Toolbox.")
    jetbrainsToolboxExtractLocation = tempfile.NamedTemporaryFile().name
    file = tarfile.open(jetbrainsToolboxDownloadLocation)
    file.extractall(jetbrainsToolboxExtractLocation)

    # Run Jetbrains Toolbox.
    print("Running Jetbrains Toolbox.")
    runProcess([jetbrainsToolboxExtractLocation + "/" + os.listdir(jetbrainsToolboxExtractLocation)[0] + "/jetbrains-toolbox"])

# Create the desktop icon for Jetbrains Toolbox.
jetbrainsToolboxShortcutLocation = localApplicationsDirectory + "jetbrains-toolbox.desktop"
if not os.path.exists(jetbrainsToolboxShortcutLocation):
    print("Creating Jetbrains Toolbox desktop icon.")
    with open(jetbrainsToolboxShortcutLocation, "w") as file:
        file.write("[Desktop Entry]\r\n")
        file.write("Version=1.0\r\n")
        file.write("Type=Application\r\n")
        file.write("Name=Jetbrains Toolbox\r\n")
        file.write("Icon=" + jetbrainsToolboxInstallLocation + "/toolbox.svg\r\n")
        file.write("Exec=" + jetbrainsToolboxInstallLocation + "/bin/jetbrains-toolbox\r\n")
        file.write("Categories=Development;")

# Install Rojo.
if not pathFileExists("rojo"):
    runProcess(["rustup", "default", "stable"])
    runProcess(["cargo", "install", "rojo"])

# Set git to use vim.
runProcess(["git", "config", "--global", "core.editor", "vim"])

# Add to the user environment.
for environmentFile in ["~/.bashrc", "~/.zshrc"]:
    environmentFile = os.path.expanduser(environmentFile)
    with open(environmentFile) as readFile:
        environmentFileContents = readFile.read()
        changesMade = False
        for additionalPath in ["$HOME/.cargo/bin/"]:
            additionalLine = "export PATH=\"$PATH:" + additionalPath + "\""
            if additionalLine not in environmentFileContents:
                environmentFileContents += "\n" + additionalLine
                changesMade = True
        if changesMade:
            with open(environmentFile, "w") as writeFile:
                writeFile.write(environmentFileContents)

# Set the desktop background.
# From: https://superuser.com/questions/488232/how-to-set-kde-desktop-wallpaper-from-command-line
desktopParentDirectory = os.path.expanduser("~/.local/share/desktop")
desktopBackgroundPath = os.path.expanduser("~/.local/share/desktop/DesktopBackground.png")
if not os.path.exists(desktopParentDirectory):
    os.makedirs(desktopParentDirectory)
if not os.path.exists(desktopBackgroundPath):
    shutil.copy(os.path.realpath(os.path.join(__file__, "..", "resources", "DesktopBackground.png")), desktopBackgroundPath)
    os.system("qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'var allDesktops = desktops();print (allDesktops);for (i=0;i<allDesktops.length;i++) {d = allDesktops[i];d.wallpaperPlugin = \"org.kde.image\";d.currentConfigGroup = Array(\"Wallpaper\", \"org.kde.image\", \"General\");d.writeConfig(\"Image\", \"file://" + desktopBackgroundPath + "\")}'")
    os.system("kwriteconfig5 --file kscreenlockerrc --group Greeter --group Wallpaper --group org.kde.image --group General --key Image \"file://" + desktopBackgroundPath + "\"")

    # Set the theme.
    # This is done with the background to reduce extra theme changes.
    os.system("lookandfeeltool -a org.kde.breezedark.desktop")

# Run the extra user setup, if there is any.
extraUserSetupPath = os.path.realpath(os.path.join(__file__, "..", "extra", "ExtraUserSetup.py"))
if os.path.exists(extraUserSetupPath):
    subprocess.Popen([sys.executable, extraUserSetupPath]).wait()
