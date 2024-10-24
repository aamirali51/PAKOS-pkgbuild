#!/bin/bash

# Check if the user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Get the directory of the script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find all ISO files in the script's directory
iso_files=("$script_dir"/*.iso)

# Check if any ISO files were found
if [ ${#iso_files[@]} -eq 0 ]; then
    echo "No ISO files found in $script_dir."
    exit 1
fi

# List available ISO files
echo "Found ISO files:"
for i in "${!iso_files[@]}"; do
    echo "$i: ${iso_files[$i]}"
done

# Ask the user to select an ISO file
read -p "Enter the number of the ISO file you want to write: " iso_index

# Validate selection
if ! [[ "$iso_index" =~ ^[0-9]+$ ]] || [ "$iso_index" -lt 0 ] || [ "$iso_index" -ge "${#iso_files[@]}" ]; then
    echo "Invalid selection."
    exit 1
fi

# Set the selected ISO file
iso_file="${iso_files[$iso_index]}"

# Automatically find USB drives
usb_device=$(lsblk -o NAME,TYPE,SIZE | grep -w 'disk' | grep -v 'loop' | grep -v 'part' | awk '{print $1}' | head -n 1)

if [ -z "$usb_device" ]; then
    echo "No USB drives found."
    exit 1
fi

# Full device path
usb_device="/dev/$usb_device"

# List available drives
echo "Selected USB drive: $usb_device"

# Double check that the user wants to continue
read -p "WARNING: All data on $usb_device will be erased! Are you sure you want to continue? (y/n) " confirmation
if [[ "$confirmation" != "y" ]]; then
    echo "Aborted."
    exit 1
fi

# Unmount all partitions on the device
echo "Unmounting all partitions on $usb_device..."
umount ${usb_device}* 2>/dev/null

# Format the USB drive
echo "Formatting $usb_device to FAT32..."
mkfs.vfat -F 32 $usb_device

# Write the ISO to the USB drive
echo "Writing $iso_file to $usb_device..."
dd if="$iso_file" of="$usb_device" bs=4M status=progress oflag=sync

# Sync to ensure data is written
sync

echo "Done! The USB drive is ready."
