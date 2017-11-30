import recalboxFiles
from generators.Generator import Generator
import os.path
import glob
import sys
import shutil
import amiberryController
import amiberryConfig
from settings.unixSettings import UnixSettings

amiberryPath="/recalbox/share/emulateurs/amiga/amiberry"
mountPoint="/tmp/amiga"
biosPath="/recalbox/share/bios/"

def generateAdf(fullName,romPath,uaeName,amigaHardware,controller) :
    print("execute ADF : <%s> on <%s>" %(amiberryPath+"/amiberry",romPath + "/" + uaeName))
    
    amiberryConfig.initMountpoint(mountPoint,amiberryPath)
    
    # ----- Create uae configuration file -----
    uaeconfig = os.path.join(mountPoint,"amiberry","conf","uaeconfig.uae")
    
    if os.path.exists(uaeconfig) :
        os.remove(uaeconfig)
    
    fUaeConfig = UnixSettings(uaeconfig, separator='', defaultComment=';')
    amiberryController.generateControllerConf(fUaeConfig)
    amiberryController.generateSpecialKeys(fUaeConfig,controller)
    amiberryConfig.generateGUIConf(fUaeConfig)
    amiberryConfig.generateKickstartPath(fUaeConfig,amigaHardware)
    amiberryConfig.generateHardwareConf(fUaeConfig,amigaHardware)
    floppiesManagement(fUaeConfig,romPath,uaeName)
    amiberryConfig.generateGraphicConf(fUaeConfig)

def floppiesManagement(fUaeConfig,romPath,uaeName) :
    # ----- Floppies management -----
    indexDisk = uaeName.rfind("Disk 1")
    
    if indexDisk == -1 :
        # Mono disk
        fUaeConfig.save("floppy0",os.path.join(romPath,uaeName))
        print("Added %s as floppy0" % os.path.join(romPath,uaeName))
        fUaeConfig.save("floppy0type","0")
        fUaeConfig.save("nr_floppies","1")
        print("Number of floppies : 1")
    
    else :
        # Several disks
        prefix = uaeName[0:indexDisk+4]
        prefixed = sorted([filename for filename in os.listdir(romPath) if filename.startswith(prefix)])
        for i in range(0,min(4,len(prefixed))) :
            fUaeConfig.save("floppy"+`i`,os.path.join(romPath,prefixed[i]))
            print("Added %s as floppy%i" % (os.path.join(romPath,prefixed[i]),i))
            fUaeConfig.save("floppy"+`i`+"type","0")
        
        nbFloppies=min(4,len(prefixed))
        fUaeConfig.save("nr_floppies",`nbFloppies`)
        print("Number of floppies : "+`nbFloppies`)

