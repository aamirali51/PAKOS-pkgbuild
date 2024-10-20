import os
import shutil
from tqdm import tqdm

# Get the directory where the script is placed
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the base destination as a local 'etc/skel' in the script's directory
dest_base = os.path.join(script_dir, "etc/skel")

# Define the source directories from the running system (excluding 'icons')
source_dirs = {
    'plasma_desktoptheme': os.path.expanduser("~/.local/share/plasma/desktoptheme/"),
    'plasma_lookandfeel': os.path.expanduser("~/.local/share/plasma/look-and-feel/"),
    'color_schemes': os.path.expanduser("~/.local/share/color-schemes/"),
    'wallpapers': os.path.expanduser("~/.local/share/wallpapers/"),
    'desktop_widgets': os.path.expanduser("~/.local/share/plasma/plasmoids/"),
    'konsole_profiles': os.path.expanduser("~/.local/share/konsole/"),
    'dolphin_settings': os.path.expanduser("~/.config/dolphinrc"),
    'sddm_theme': '/usr/share/sddm/themes/',  # SDDM themes are system-wide
    'window_decorations': os.path.expanduser("~/.local/share/aurorae/themes/"),  # Window decoration themes
    'kvantum_themes': os.path.expanduser("~/.local/share/Kvantum/"),  # Kvantum themes
    'config_files': {
        'plasma-applets': os.path.expanduser("~/.config/plasma-org.kde.plasma.desktop-appletsrc"),
        'kdeglobals': os.path.expanduser("~/.config/kdeglobals"),
        'kwin': os.path.expanduser("~/.config/kwinrc"),
        'kscreenlocker': os.path.expanduser("~/.config/kscreenlockerrc"),
        'latte': os.path.expanduser("~/.config/latte/"),  # if using Latte Dock
        'kvantum_config': os.path.expanduser("~/.config/Kvantum/"),  # Kvantum config folder (includes kvantum.kvconfig and themes)
        'ksplash': os.path.expanduser("~/.config/ksplashrc")  # KDE Plasma splash screen settings
    }
}

# Define the destination directories relative to 'etc/skel' in the script's folder (excluding 'icons')
dest_dirs = {
    'plasma_desktoptheme': os.path.join(dest_base, ".local/share/plasma/desktoptheme/"),
    'plasma_lookandfeel': os.path.join(dest_base, ".local/share/plasma/look-and-feel/"),
    'color_schemes': os.path.join(dest_base, ".local/share/color-schemes/"),
    'wallpapers': os.path.join(dest_base, ".local/share/wallpapers/"),
    'desktop_widgets': os.path.join(dest_base, ".local/share/plasma/plasmoids/"),
    'konsole_profiles': os.path.join(dest_base, ".local/share/konsole/"),
    'dolphin_settings': os.path.join(dest_base, ".config/dolphinrc"),
    'sddm_theme': os.path.join(dest_base, "usr/share/sddm/themes/"),
    'window_decorations': os.path.join(dest_base, ".local/share/aurorae/themes/"),
    'kvantum_themes': os.path.join(dest_base, ".local/share/Kvantum/"),  # Kvantum themes
    'config_files': {
        'plasma-applets': os.path.join(dest_base, ".config/plasma-org.kde.plasma.desktop-appletsrc"),
        'kdeglobals': os.path.join(dest_base, ".config/kdeglobals"),
        'kwin': os.path.join(dest_base, ".config/kwinrc"),
        'kscreenlocker': os.path.join(dest_base, ".config/kscreenlockerrc"),
        'latte': os.path.join(dest_base, ".config/latte/"),
        'kvantum_config': os.path.join(dest_base, ".config/Kvantum/"),  # Kvantum config destination
        'ksplash': os.path.join(dest_base, ".config/ksplashrc")  # KDE Plasma splash screen destination
    }
}

# Function to copy files with progress and error handling
def copy_with_progress(src, dest):
    try:
        # If the source is a directory, use shutil.copytree
        if os.path.isdir(src):
            file_count = sum(len(files) for _, _, files in os.walk(src))
            with tqdm(total=file_count, desc=f"Copying {os.path.basename(src)}") as pbar:
                shutil.copytree(src, dest, dirs_exist_ok=True, copy_function=lambda s, d: (shutil.copy2(s, d), pbar.update())[1])
        # If it's a file, just copy it directly
        elif os.path.isfile(src):
            tqdm.write(f"Copying {os.path.basename(src)}")
            shutil.copy2(src, dest)
            tqdm.write(f"{os.path.basename(src)} copied successfully")
    except Exception as e:
        tqdm.write(f"Error copying {src}: {e}")

def copy_theming_files():
    # Copy Plasma themes, wallpapers, window decorations, Kvantum themes, and color schemes (excluding 'icons')
    for key, src in source_dirs.items():
        if key != 'config_files':
            dest = dest_dirs[key]
            if os.path.exists(src):
                if not os.path.exists(dest):
                    os.makedirs(dest)
                copy_with_progress(src, dest)
            else:
                tqdm.write(f"Skipped: {src} (not found)")

    # Copy KDE configuration files, including Kvantum folder and ksplashrc
    for config, src in source_dirs['config_files'].items():
        dest = dest_dirs['config_files'][config]
        if os.path.exists(src):
            dest_folder = os.path.dirname(dest)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            copy_with_progress(src, dest)
        else:
            tqdm.write(f"Skipped: {src} (not found)")

if __name__ == "__main__":
    copy_theming_files()
