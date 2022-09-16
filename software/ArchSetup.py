"""
TheNexusAvenger

Setup specific for Arch Linux.
"""

import os
import re
import shutil
import subprocess
from helper.Path import pathFileExists
from helper.Process import runProcess
from software.PackageManager import getPackageManager


def setUpArch():
    """Sets up specifics for Arch Linux.
    """

    # Enable parallel downloads for pacman.
    # TODO: Enable multilib for Grapejuice for distros that disable by default. Manjaro enables this by default.
    if os.path.exists("/etc/pacman.conf"):
        with open("/etc/pacman.conf") as readFile:
            pacmanConfFile = readFile.read()
            if "#ParallelDownloads" in pacmanConfFile:
                pacmanConfFile = pacmanConfFile.replace("#ParallelDownloads", "ParallelDownloads")
                with open("/etc/pacman.conf", "w") as writeFile:
                    writeFile.write(pacmanConfFile)

    # Install Yay for installing from the Arch User Repository (AUR).
    # Due to permission issues, this is done in a new Konsole window.
    if not pathFileExists("yay"):
        getPackageManager("pacman").installPackages(["git", "base-devel"])
        if not os.path.exists("/var/tmp/yay-install.sh"):
            with open("/var/tmp/yay-install.sh", "w") as file:
                file.write("git clone https://aur.archlinux.org/yay-bin.git /var/tmp/yay-bin\n")
                file.write("cd /var/tmp/yay-bin\n")
                file.write("makepkg -si")
        runProcess(["su", os.environ["SUDO_USER"], "-c", "konsole -e \"source /var/tmp/yay-install.sh\""])

    # Set up Secure Boot.
    # TODO: This is incomplete. Potentially missing something for key registration.
    if not pathFileExists("/boot/efi/EFI/BOOT/grubx64.efi"):
        # Find the boot partitions.
        efiPartition = None
        fileSystemPartition = None
        for line in subprocess.check_output(["lsblk"], stderr=subprocess.DEVNULL).decode().split("\n"):
            if "part /boot/efi" in line:
                efiPartition = re.findall(r"[a-zA-Z\d]+", line)[0]
            elif "part /" in line:
                fileSystemPartition = re.findall(r"[a-zA-Z\d]+", line)[0]

        # Determine the boot drive and partition number.
        partitionSameName = ""
        efiPartitionDifference = ""
        for i in range(0, len(efiPartition)):
            character = efiPartition[i]
            if efiPartitionDifference != "" or character != fileSystemPartition[i]:
                efiPartitionDifference += character
            else:
                partitionSameName += character
        if partitionSameName.startswith("nvme") and partitionSameName.endswith("p"):
            partitionSameName = partitionSameName[0:len(partitionSameName) - 1]
        efiPartitionNumber = re.findall(r"\d+", efiPartitionDifference)[0]

        # Install shim-signed.
        aurPackageManager = getPackageManager("aur")
        if not aurPackageManager.isPackageInstalled("shim-signed"):
            aurPackageManager.installPackages(["shim-signed"])

        # Move the GRUB boot file.
        shutil.copy("/boot/efi/EFI/BOOT/bootx64.efi", "/boot/efi/EFI/BOOT/grubx64.efi")

        # Copy the shim files.
        if not os.path.exists("/boot/efi/EFI/BOOT/BOOTx64.EFI"):
            shutil.copy("/usr/share/shim-signed/shimx64.efi", "/boot/efi/EFI/BOOT/BOOTx64.EFI")
        if not os.path.exists("/boot/efi/EFI/BOOT/mmx64.efi"):
            shutil.copy("/usr/share/shim-signed/mmx64.efi", "/boot/efi/EFI/BOOT/mmx64.efi")

        # Create the NVRAM entry.
        runProcess(["efibootmgr", "--verbose", "--disk", "/dev/" + partitionSameName, "--part", str(efiPartitionNumber), "--create", "--label", "Arch Secure Boot Shim", "--loader", "/EFI/BOOT/BOOTx64.EFI"])