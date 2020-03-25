#!/usr/bin/env python3

################################################################################
# This script is for quickly creating ssh tunnels
# Copyright (C) 2014  Rachel Domagalski: github.com/domagalski
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
import argparse

if __name__ == "__main__":
    # Get options fromt the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("userhost", help="SSH login info.")
    parser.add_argument("-p", "--port", required=True, type=int, help="Port number to use.")
    parser.add_argument("-H", "--host", default="localhost", help="Hostname of the port to tunnel.")
    parser.add_argument("-b", "--bind", default="localhost", help="Binding address of the tunnel.")
    parser.add_argument(
        "-v",
        "--verbose",
        default=1,
        choices=range(1, 3 + 1),
        metavar="NUM",
        help="SSH verbosity level (1-3).",
    )
    args = parser.parse_args()

    port = str(args.port)
    dash_l = ":".join([args.bind, port, args.host, port])
    ssh_cmd = "ssh -" + args.verbose * "v"
    ssh_cmd += " -N -L " + dash_l + " " + args.userhost
    sys.exit(os.system(ssh_cmd))
