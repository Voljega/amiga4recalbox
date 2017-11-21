import recalboxFiles
from generators.Generator import Generator
import os.path
import glob
import sys
import shutil
import amiberryController
import amiberryConfig
from settings.unixSettings import UnixSettings

uae4armPath="/recalbox/share/emulateurs/amiga/uae4arm"
mountPoint="/tmp/amiga"
biosPath="/recalbox/share/bios/"

def generateCD(fullName,romPath,uaeName,amigaHardware,controller) :
    # TODO Also allow to use Amiga CD ?
    
    if not amiberryConfig.hasCD32Kickstarts() :
        sys.exit("No CD32 kickstarts found")
    
    print("execute CD32 : <%s> on <%s>" %(uae4armPath+"/uae4arm",romPath + "/" + uaeName))
    
    amiberryConfig.initMountpoint(mountPoint,uae4armPath)
    
    # ----- Create uae configuration file -----
    uaeconfig = os.path.join(mountPoint,"uae4arm","conf","uaeconfig.uae")
    
    if os.path.exists(uaeconfig) :
        os.remove(uaeconfig)
    
    fUaeConfig = UnixSettings(uaeconfig, separator='', defaultComment=';')
    amiberryController.generateCD32ControllerConf(fUaeConfig,controller)
    amiberryConfig.generateGUIConf(fUaeConfig,"false")
    amiberryConfig.generateKickstartPathCD32(fUaeConfig,amigaHardware)
    amiberryConfig.generateHardwareConf(fUaeConfig,amigaHardware)
    generateCD32Conf(fUaeConfig,romPath,uaeName)
    amiberryConfig.generateCD32GraphicConf(fUaeConfig)
    
def generateCD32Conf(fUaeConfig,romPath,uaeName) :
    fUaeConfig.save("cdimage0",os.path.join(romPath,uaeName)+",image")
