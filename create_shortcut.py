import os
import sys
from pathlib import Path
import win32com.client

wscript = win32com.client.Dispatch("WScript.Shell")

user_home = Path.home()
desktop_locations = [
    user_home / "Desktop",
    user_home / "OneDrive" / "Bureau",
    user_home / "OneDrive" / "Desktop",
]

base_dir = Path(__file__).resolve().parent
target_venv = base_dir / ".venv" / "Scripts" / "pythonw.exe"
target = str(target_venv if target_venv.exists() else Path(sys.executable))
args = str(base_dir / "main.py")
cwd = str(base_dir)

created = []
for loc in set(desktop_locations):
    if loc.exists():
        lnk_path = loc / "Pierre's Power Scraper.lnk"
        shortcut = wscript.CreateShortcut(str(lnk_path))
        shortcut.TargetPath = target
        shortcut.Arguments = f'"{args}"'
        shortcut.WorkingDirectory = cwd
        shortcut.Description = "Pierre's Power Scraper"
        shortcut.IconLocation = r"C:\Windows\System32\shell32.dll,238"
        shortcut.Save()
        created.append(str(lnk_path))

print("Created shortcuts:", created)
