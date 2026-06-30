"""Scanning utilities"""

import os


def scan_pacman():
    """Scans pacman cache"""
    results = {}
    path = "/var/cache/pacman/pkg"
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                base_name = entry.name.split(".pkg.tar")[0]
                package_name = base_name.rsplit("-", 3)[0]
                size = entry.stat().st_size
                if size >= 1024**2:
                    results[package_name] = f"{size // 1024**2} MB"
                elif size >= 1024:
                    results[package_name] = f"{size // 1024} KB"
                else:
                    results[package_name] = f"{size} B"
    return results
