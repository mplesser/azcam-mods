"""
Setup method for LBTO MODS azcamserver.
Usage example:
  python -i -m azcam_mods.server -- -system mods
"""

import os
import sys

import azcam
import azcam.utils
import azcam.exceptions
import azcam.server
import azcam.shortcuts
from azcam.cmdserver import CommandServer
from azcam.header import System

# from azcam.tools.ds9display import Ds9Display
from azcam.tools.telescope import Telescope
from azcam.tools.instrument import Instrument
from azcam.tools.archon.controller_archon import ControllerArchon
from azcam.tools.archon.exposure_archon import ExposureArchon
from azcam.tools.archon.tempcon_archon import TempConArchon
from azcam_mods.detector_mods import detector_mods

from azcam.web.fastapi_server import WebServer


def setup():
    # command line args
    option = "menu"
    try:
        i = sys.argv.index("-mods")
        option = "MODS"
    except ValueError:
        pass

    try:
        i = sys.argv.index("-testdewar")
        option = "testdewar"
    except ValueError:
        pass

    try:
        i = sys.argv.index("-datafolder")
        datafolder = sys.argv[i + 1]
    except ValueError:
        datafolder = None

    try:
        i = sys.argv.index("-remotehost")
        remote_host = sys.argv[i + 1]
    except ValueError:
        remote_host = None

    # for dev only
    option = "testdewar"
    azcam.db.verbosity = 2
    os.environ["AZCAM_DATAROOT"] = "/home/mods/data"

    # define folders for system
    azcam.db.systemname = "MODS"

    azcam.db.rootfolder = os.path.abspath(os.path.dirname(__file__))

    azcam.db.systemfolder = os.path.dirname(__file__)
    azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)
    azcam.db.datafolder = azcam.utils.get_datafolder(datafolder)

    # configuration menu
    menu_options = {
        "MODS": "MODS",
        "MODS test dewar": "testdewar",
    }
    if option == "menu":
        print("MODS Startup Menu\n")
        option = azcam.utils.show_menu(menu_options)

    if "MODS" in option:
        parfile = os.path.join(azcam.db.datafolder, "parameters", "parameters_mods.ini")
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_mods.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "archon",
            "mods_1.acf",
        )
        azcam.db.servermode = "archon"
        cmdport = 2402

    elif "testdewar" in option:
        parfile = os.path.join(azcam.db.datafolder, "parameters", "parameters_mods.ini")
        template = os.path.join(
            azcam.db.datafolder, "templates", "fits_template_mods.txt"
        )
        timingfile = os.path.join(
            azcam.db.datafolder,
            "archon",
            "mods_1.acf",
        )
        azcam.db.servermode = "MODS"
        cmdport = 2402

    else:
        raise azcam.exceptions.AzcamError("bad system configuration")

    # logging
    logfile = os.path.join(azcam.db.datafolder, "logs", "server.log")
    azcam.db.logger.start_logging(logfile=logfile)
    azcam.log(f"MODS mode: {option}")

    # controller
    controller = ControllerArchon()
    controller.timing_file = timingfile
    controller.camserver.port = 4242
    controller.camserver.host = "10.0.0.2"
    controller.reset_flag = 0  # 0 for soft reset, 1 to upload code
    controller.verbosity = 2

    # tempcon

    tempcon = TempConArchon(description="MODS Archon")
    tempcon.temperature_ids = [0, 2]  # camtemp, dewtemp
    tempcon.heaterx_board = "MOD1"
    tempcon.control_temperature = -95.0
    controller.heater_board_installed = 1

    # exposure
    exposure = ExposureArchon()
    exposure.filetype = exposure.filetypes["MEF"]
    exposure.image.filetype = exposure.filetypes["MEF"]
    exposure.display_image = 0
    exposure.add_extensions = 1

    exposure.image.focalplane.gains = 4 * [2.0]
    exposure.image.focalplane.rdnoises = 4 * [2.0]

    if remote_host is None:
        pass
    else:
        exposure.send_image = 1
        exposure.sendimage.set_remote_imageserver(remote_host, 6543, "azcam")

    # instrument
    instrument = Instrument()

    # telescope
    telescope = Telescope()

    # system header template
    system = System("MODS", template)
    system.set_keyword("DETNAME", "MODS", "Detector name")

    # detector

    exposure.set_detpars(detector_mods)
    exposure.fileconverter.set_detector_config(detector_mods)

    # display
    # display = Ds9Display()

    # parameter file
    azcam.db.parameters.read_parfile(parfile)
    azcam.db.parameters.update_pars()

    # command server
    cmdserver = CommandServer()
    cmdserver.port = cmdport
    azcam.log(f"Starting cmdserver - listening on port {cmdserver.port}")
    azcam.db.tools["api"].initialize_api()
    cmdserver.start()

    # web server
    if 0:
        webserver = WebServer()
        webserver.logcommands = 0
        webserver.port = 2403
        webserver.start()

    # azcammonitor
    if 0:
        azcam.db.monitor.register()

    # finish
    azcam.log("Configuration complete")


# start
setup()
from azcam.cli import *
