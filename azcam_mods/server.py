"""
Setup method for LBTO MODS azcamserver.
Usage example:
  python -i -m azcam_mods.server -- -system archon
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
from azcam.tools.ds9display import Ds9Display
from azcam.tools.telescope import Telescope
from azcam.tools.instrument import Instrument
from azcam.tools.archon.controller_archon import ControllerArchon
from azcam.tools.archon.exposure_archon import ExposureArchon
from azcam.tools.archon.tempcon_archon import TempConArchon
from azcam_mods.detector_mods import detector_mods_test_dewar, detector_mods

from azcam.webtools.webserver import WebServer
from azcam.webtools.status.status import Status
from azcam.webtools.exptool.exptool import Exptool


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
            "mods_testdewar_1.acf",
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
    controller.camserver.host = "10.30.3.6"
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
    # exposure.update_headers_in_background = 1
    exposure.display_image = 0
    exposure.add_extensions = 1

    exposure.image.focalplane.gains = 4 * [2.9]
    exposure.image.focalplane.rdnoises = 4 * [4.0]

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
    display = Ds9Display()

    # system-specific
    sc = 0.000125
    exposure.image.focalplane.wcs.scale1 = 4 * [-1 * sc]
    exposure.image.focalplane.wcs.scale2 = 4 * [-1 * sc]
    exposure.image.focalplane.wcs.rot_deg = 4 * [90.0]

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
    if 1:
        webserver = WebServer()
        webserver.logcommands = 0
        webserver.index = os.path.join(azcam.db.systemfolder, "index_MODS.html")
        webserver.port = 2403
        webserver.start()

        webstatus = Status(webserver)
        webstatus.initialize()

        exptool = Exptool(webserver)
        exptool.initialize()

    # azcammonitor
    azcam.db.monitor.proc_path = "/azcam/azcam-mods/support/start_server_mods.py"
    azcam.db.monitor.register()

    # GUIs
    if 0:
        if os.name != "posix":
            import azcam_90prime.start_azcamtool

    # finish
    azcam.log("Configuration complete")


# start
setup()
from azcam.cli import *
