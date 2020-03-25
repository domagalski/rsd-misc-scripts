#!/usr/bin/env python3

import glob
import pathlib
from typing import Dict, List

import psutil

VNC_PORT_BASE = 5900

def get_vnc_pids() -> Dict[int, int]:
    vnc_dir = pathlib.Path.home() / ".vnc"
    pid_dict = {}
    for pid_file in vnc_dir.glob("**/*.pid"):
        vnc_num = int(pid_file.stem.split(":")[-1])

        with pid_file.open() as f:
            pid_num = int(f.read().strip())

        pid_dict[vnc_num] = pid_num

    return pid_dict

def check_pids(pid_dict: Dict[int, int]) -> List[int]:
    vnc_list = []
    for vnc in pid_dict:
        pid = pid_dict[vnc]
        if not psutil.pid_exists(pid):
            continue

        proc = psutil.Process(pid)
        if proc.name() in ["Xvnc", "Xvnc4"]:
            vnc_list.append(vnc)

    return vnc_list

if __name__ == "__main__":
    active_vnc = check_pids(get_vnc_pids())
    if active_vnc:
        print("Active VNC (remote desktop) instances:")
        for vnc in sorted(active_vnc):
            port = VNC_PORT_BASE + vnc
            print(f"\tDisplay :{vnc} active on port {port}.")
    else:
        print("No active VNC (remote desktop) instances.")
