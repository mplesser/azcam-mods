"""
Python process start file
"""

import subprocess

OPTIONS = "-mods2b"
# CMD = f"ipython --ipython-dir=~/data/ipython --profile azcamconsole -i -m azcam_mods.console -- {OPTIONS}"
CMD = f"ipython --ipython-dir=/data/ipython --profile azcamconsole -i -m azcam_mods.console -- {OPTIONS}"

p = subprocess.Popen(
    CMD,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
