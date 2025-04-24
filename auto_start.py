import os
import sys
import shutil
import winreg as reg

def add_to_startup(script_path=None):
    if script_path is None:
        script_path = os.path.realpath(sys.argv[0])

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "FaceLockSystem"

    with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
        reg.SetValueEx(registry_key, name, 0, reg.REG_SZ, script_path)
