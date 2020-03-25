#!/usr/bin/env python3

################################################################################
# This script is for connecting to VNC clients via ssh tunneling.
# Copyright (C) 2020 Rachel Domagalski: github.com/domagalski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import os
import sys
import time
import socket
import tkinter as tk
import subprocess as spr


class VNCparams:
    def __init__(self, parent):
        """
        Create a simple interface to get user input.
        """
        self.top = tk.Frame(parent)
        self.top.pack()
        tk.Label(self.top, text="SSH connection").pack()
        self.ssh_field = tk.Entry(self.top)
        self.ssh_field.pack(padx=5)
        tk.Label(self.top, text="Display").pack()
        self.display_field = tk.Entry(self.top)
        self.display_field.pack(padx=5)

        b = tk.Button(self.top, text="OK", command=self.get_pars)
        b.pack(pady=5)

        # Store the form values in these variables
        self.ssh = None
        self.display = None

    def get_pars(self):
        """
        Grab user input, check it, and save it.
        """
        # Get the input from the fields.
        self.ssh = self.ssh_field.get()
        self.display = self.display_field.get()
        error = False

        # Check that the input was provided.
        if self.ssh is None or self.ssh == "":
            error = self.raise_error("ERROR: No ssh connection info provided.")
        if self.display is None or self.display == "":
            error = self.raise_error("ERROR: No display provided.")
        if error:
            return

        # Check that the display is an integer and valid
        try:
            self.display = int(self.display)
            if self.display < 0 or self.display > 255:
                error = self.raise_error("ERROR: Display is out of range.")
        except ValueError:
            error = self.raise_error("ERROR: Display must be an integer.")
        if not error:
            self.top.destroy()

    def raise_error(self, err_msg):
        """
        Raise a window with an error and exit.
        """
        tk.Label(self.top, text=err_msg).pack()
        return True


def get_ip(display):
    """
    Get the IP address that the VNC server gets bound to.
    """
    return "127.0.0." + str(max(display, 1))


def tunnel(ssh, display, srv="localhost"):
    """
    Create the SSH tunnel.
    """
    # Open a SSH tunnel.
    port = str(5900 + display)
    bind = get_ip(display)
    cmd = ["ssh", "-N", "-L", ":".join([bind, port, srv, port]), ssh]
    proc = spr.Popen(cmd)

    # Check the tunnel connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while sock.connect_ex((bind, int(port))):
        exit_status = proc.poll()
        if exit_status:
            sys.exit(exit_status)
        time.sleep(0.1)

    # Cleanup and return the tunnel process
    sock.close()
    return proc


def vnc_client(display):
    """
    Run the VNC client.
    """
    server = get_ip(display) + ":" + str(display)
    cmd = " ".join(["vncviewer", server])
    return os.system(cmd)


if __name__ == "__main__":
    # Get input from the user.
    root = tk.Tk()
    root.title("VNC\t")
    params = VNCparams(root)
    root.wait_window(params.top)
    try:
        root.destroy()
    except tk.TclError:
        sys.exit(1)

    # Run the VNC client
    tun = tunnel(params.ssh, params.display)
    status = vnc_client(params.display)
    tun.kill()
    sys.exit(status)
