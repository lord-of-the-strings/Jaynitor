"""Scanning utilities"""

import asyncio
import os


def scan_pacman():
    """Scans pacman cache"""
    results = {}
    raw = {}
    path = "/var/cache/pacman/pkg"
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                base_name = entry.name.split(".pkg.tar")[0]
                package_name = base_name.rsplit("-", 3)[0]
                try:
                    size = raw[package_name] + entry.stat().st_size
                except KeyError:
                    size = entry.stat().st_size
                raw[package_name] = size
                if size >= 1024**2:
                    results[package_name] = f"{size // 1024**2} MB"
                elif size >= 1024:
                    results[package_name] = f"{size // 1024} KB"
                else:
                    results[package_name] = f"{size} B"
    return results


async def clear_pacman():
    """Runs paccache"""
    try:
        p = await asyncio.create_subprocess_exec(
            "sudo",
            "paccache",
            "-rk0",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await p.communicate()
        if p.returncode == 0:
            txt = stdout.decode().strip()
            return txt
        else:
            err = stderr.decode().strip()
            return f"Error: {err}"
    except Exception as e:
        return str(e)
