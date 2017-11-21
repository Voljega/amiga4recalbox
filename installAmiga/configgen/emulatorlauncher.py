#!/usr/bin/env python

import argparse
import time
import sys
from sys import exit
from Emulator import Emulator
import generators
from generators.fba2x.fba2xGenerator import Fba2xGenerator
from generators.kodi.kodiGenerator import KodiGenerator
from generators.linapple.linappleGenerator import LinappleGenerator
from generators.libretro.libretroGenerator import LibretroGenerator
from generators.moonlight.moonlightGenerator import MoonlightGenerator
from generators.mupen.mupenGenerator import MupenGenerator
from generators.ppsspp.ppssppGenerator import PPSSPPGenerator
from generators.reicast.reicastGenerator import ReicastGenerator
from generators.dolphin.dolphinGenerator import DolphinGenerator
from generators.scummvm.scummvmGenerator import ScummVMGenerator
from generators.dosbox.dosboxGenerator import DosBoxGenerator
from generators.vice.viceGenerator import ViceGenerator
from generators.advancemame.advMameGenerator import AdvMameGenerator
from generators.amiberry.amiberryGenerator import AmiberryGenerator
import controllersConfig as controllers
import utils.runner as runner
import signal
import recalboxFiles
import os

generators = {
    'fba2x': Fba2xGenerator(),
    'kodi': KodiGenerator(),
    'linapple': LinappleGenerator(os.path.join(recalboxFiles.HOME_INIT, '.linapple'),
                                  os.path.join(recalboxFiles.HOME, '.linapple')),
    'libretro': LibretroGenerator(),
    'moonlight': MoonlightGenerator(),
    'scummvm': ScummVMGenerator(),
    'dosbox': DosBoxGenerator(),
    'mupen64plus': MupenGenerator(),
    'vice': ViceGenerator(),
    'reicast': ReicastGenerator(),
    'dolphin': DolphinGenerator(),
    'ppsspp': PPSSPPGenerator(),
    'advancemame' : AdvMameGenerator(),
	'amiberry': AmiberryGenerator()
}

# List emulators with their cores rest mupen64, scummvm
emulators = dict()
# Nintendo
emulators["snes"] = Emulator(name='snes', emulator='libretro', core='pocketsnes')
emulators["nes"] = Emulator(name='nes', emulator='libretro', core='fceunext')
emulators["n64"] = Emulator(name='n64', emulator='mupen64plus', core='gliden64')
emulators["gba"] = Emulator(name='gba', emulator='libretro', core='gpsp')
emulators["gb"] = Emulator(name='gb', emulator='libretro', core='gambatte')
emulators["gbc"] = Emulator(name='gbc', emulator='libretro', core='gambatte')
emulators["fds"] = Emulator(name='fds', emulator='libretro', core='nestopia')
emulators["virtualboy"] = Emulator(name='virtualboy', emulator='libretro', core='vb')
emulators["gamecube"] = Emulator(name='gamecube', emulator='dolphin')
emulators["wii"] = Emulator(name='wii', emulator='dolphin')
# Sega
emulators["sg1000"] = Emulator(name='sg1000', emulator='libretro', core='genesisplusgx')
emulators["mastersystem"] = Emulator(name='mastersystem', emulator='libretro', core='picodrive')
emulators["megadrive"] = Emulator(name='megadrive', emulator='libretro', core='picodrive')
emulators["gamegear"] = Emulator(name='gamegear', emulator='libretro', core='genesisplusgx')
emulators["sega32x"] = Emulator(name='sega32x', emulator='libretro', core='picodrive')
emulators["segacd"] = Emulator(name='segacd', emulator='libretro', core='picodrive')
emulators["dreamcast"] = Emulator(name='dreamcast', emulator='reicast')
# Arcade
emulators["neogeo"] = Emulator(name='neogeo', emulator='fba2x')
emulators["mame"] = Emulator(name='mame', emulator='libretro', core='mame078')
emulators["fba"] = Emulator(name='fba', emulator='fba2x')
emulators["fba_libretro"] = Emulator(name='fba_libretro', emulator='libretro', core='fba')
emulators["advancemame"] = Emulator(name='advancemame', emulator='advmame')
# Computers
emulators["msx"] = Emulator(name='msx', emulator='libretro', core='bluemsx')
emulators["msx1"] = Emulator(name='msx1', emulator='libretro', core='bluemsx')
emulators["msx2"] = Emulator(name='msx2', emulator='libretro', core='bluemsx')
emulators["amiga"] = Emulator(name='amiga', emulator='libretro', core='puae')
emulators["amstradcpc"] = Emulator(name='amstradcpc', emulator='libretro', core='cap32')
emulators["apple2"] = Emulator(name='apple2', emulator='linapple', videomode='default')
emulators["atarist"] = Emulator(name='atarist', emulator='libretro', core='hatari')
emulators["zxspectrum"] = Emulator(name='zxspectrum', emulator='libretro', core='fuse')
emulators["o2em"] = Emulator(name='odyssey2', emulator='libretro', core='o2em')
emulators["zx81"] = Emulator(name='zx81', emulator='libretro', core='81')
emulators["dos"] = Emulator(name='dos', emulator='dosbox', videomode='default')
emulators["c64"] = Emulator(name='c64', emulator='libretro', core='vice_x64')
#
emulators["ngp"] = Emulator(name='ngp', emulator='libretro', core='mednafen_ngp')
emulators["ngpc"] = Emulator(name='ngpc', emulator='libretro', core='mednafen_ngp')
emulators["gw"] = Emulator(name='gw', emulator='libretro', core='gw')
emulators["vectrex"] = Emulator(name='vectrex', emulator='libretro', core='vecx')
emulators["lynx"] = Emulator(name='lynx', emulator='libretro', core='handy')
emulators["lutro"] = Emulator(name='lutro', emulator='libretro', core='lutro')
emulators["wswan"] = Emulator(name='wswan', emulator='libretro', core='mednafen_wswan', ratio='16/10')
emulators["wswanc"] = Emulator(name='wswanc', emulator='libretro', core='mednafen_wswan', ratio='16/10')
emulators["pcengine"] = Emulator(name='pcengine', emulator='libretro', core='mednafen_supergrafx')
emulators["pcenginecd"] = Emulator(name='pcenginecd', emulator='libretro', core='mednafen_supergrafx')
emulators["supergrafx"] = Emulator(name='supergrafx', emulator='libretro', core='mednafen_supergrafx')
emulators["atari2600"] = Emulator(name='atari2600', emulator='libretro', core='stella')
emulators["atari7800"] = Emulator(name='atari7800', emulator='libretro', core='prosystem')
emulators["prboom"] = Emulator(name='prboom', emulator='libretro', core='prboom')
emulators["psx"] = Emulator(name='psx', emulator='libretro', core='pcsx_rearmed')
emulators["cavestory"] = Emulator(name='cavestory', emulator='libretro', core='nxengine')
emulators["imageviewer"] = Emulator(name='imageviewer', emulator='libretro', core='imageviewer')
emulators["scummvm"] = Emulator(name='scummvm', emulator='scummvm', videomode='default')
emulators["colecovision"] = Emulator(name='colecovision', emulator='libretro', core='bluemsx')
emulators["amiga600"] = Emulator(name='amiga600', emulator='amiberry')
emulators["amiga1200"] = Emulator(name='amiga1200', emulator='amiberry')
emulators["amigacd32"] = Emulator(name='amigacd32', emulator='amiberry')

emulators["kodi"] = Emulator(name='kodi', emulator='kodi', videomode='default')
emulators["moonlight"] = Emulator(name='moonlight', emulator='moonlight')
emulators["psp"] = Emulator(name='psp', emulator='ppsspp')


def main(args):
    playersControllers = dict()
    if not args.demo:
        # Read the controller configuration
        playersControllers = controllers.loadControllerConfig(args.p1index, args.p1guid, args.p1name, args.p1devicepath, args.p1nbaxes,
                                                              args.p2index, args.p2guid, args.p2name, args.p2devicepath, args.p2nbaxes,
                                                              args.p3index, args.p3guid, args.p3name, args.p3devicepath, args.p3nbaxes,
                                                              args.p4index, args.p4guid, args.p4name, args.p4devicepath, args.p4nbaxes,
                                                              args.p5index, args.p5guid, args.p5name, args.p5devicepath, args.p5nbaxes)

    systemName = args.system
    # Main Program
    # A generator will configure its emulator, and return a command
    if systemName in emulators:
        system = emulators[systemName]
        system.configure(args.emulator, args.core, args.ratio, args.netplay)

        # Save dir
        dirname = os.path.join(recalboxFiles.savesDir, system.name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
        
        if system.config['emulator'] not in recalboxFiles.recalboxBins:
            strErr = "ERROR : {} is not a known emulator".format(system.config['emulator'])
            print >> sys.stderr, strErr
            exit(2)
        
        command = generators[system.config['emulator']].generate(system, args.rom, playersControllers)
        # The next line is commented and will eventually be used instead of the previous one
        # if we even want the binary to be set from here rather than from the generator
        # command.array.insert(0, recalboxFiles.recalboxBins[system.config['emulator']])
        print(command)
        return runner.runCommand(command)
    
    else:
        sys.stderr.write("Unknown system: {}".format(systemName))
        return 1

def config_upgrade(version):
    '''
    Upgrade all generators user's configuration files with new values added
    to their system configuration file upgraded by S11Share:do_upgrade()
    
    Args: 
        version (str): New Recalbox version
        
    Returns (bool):
        Returns True if all generators sucessfully handled the upgraded.
    '''
    res = True
    for g in generators.values():
        res &= g.config_upgrade(version)
    return res

def signal_handler(signal, frame):
    print('Exiting')
    if runner.proc:
        print('killing runner.proc')
        runner.proc.kill()
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='emulator-launcher script')
    parser.add_argument("-p1index", help="player1 controller index", type=int, required=False)
    parser.add_argument("-p1guid", help="player1 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p1name", help="player1 controller name", type=str, required=False)
    parser.add_argument("-p1devicepath", help="player1 controller device", type=str, required=False)
    parser.add_argument("-p1nbaxes", help="player1 controller number of axes", type=str, required=False)
    parser.add_argument("-p2index", help="player2 controller index", type=int, required=False)
    parser.add_argument("-p2guid", help="player2 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p2name", help="player2 controller name", type=str, required=False)
    parser.add_argument("-p2devicepath", help="player2 controller device", type=str, required=False)
    parser.add_argument("-p2nbaxes", help="player2 controller number of axes", type=str, required=False)
    parser.add_argument("-p3index", help="player3 controller index", type=int, required=False)
    parser.add_argument("-p3guid", help="player3 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p3name", help="player3 controller name", type=str, required=False)
    parser.add_argument("-p3devicepath", help="player3 controller device", type=str, required=False)
    parser.add_argument("-p3nbaxes", help="player3 controller number of axes", type=str, required=False)
    parser.add_argument("-p4index", help="player4 controller index", type=int, required=False)
    parser.add_argument("-p4guid", help="player4 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p4name", help="player4 controller name", type=str, required=False)
    parser.add_argument("-p4devicepath", help="player4 controller device", type=str, required=False)
    parser.add_argument("-p4nbaxes", help="player4 controller number of axes", type=str, required=False)
    parser.add_argument("-p5index", help="player5 controller index", type=int, required=False)
    parser.add_argument("-p5guid", help="player5 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p5name", help="player5 controller name", type=str, required=False)
    parser.add_argument("-p5devicepath", help="player5 controller device", type=str, required=False)
    parser.add_argument("-p5nbaxes", help="player5 controller number of axes", type=str, required=False)
    parser.add_argument("-system", help="select the system to launch", type=str, required=True)
    parser.add_argument("-rom", help="rom absolute path", type=str, required=True)
    parser.add_argument("-emulator", help="force emulator", type=str, required=False)
    parser.add_argument("-core", help="force emulator core", type=str, required=False)
    parser.add_argument("-ratio", help="force game ratio", type=str, required=False)
    parser.add_argument("-demo", help="mode demo", type=bool, required=False)
    parser.add_argument("-netplay", help="host/client", type=str, required=False)

    args = parser.parse_args()
    exitcode = main(args)
    time.sleep(1)
    exit(exitcode)
    

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
