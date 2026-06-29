import shutil


def calculate():
    total, used, free = shutil.disk_usage("/")
    gb = 1024**3
    total_gb = total // gb
    used_gb = used // gb
    free_gb = free // gb
    percent = int(used / total * 100)
    return {
        "percentage": percent,
        "ui": f"Total: {total_gb} GB | Used: {used_gb} GB ({percent})% | Free: {free_gb} GB",
    }
