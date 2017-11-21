import recalboxFiles
from generators.Generator import Generator
import os.path
import glob
import sys
import shutil
import amiberryController
import sys
import amiberryConfig
import binascii
from settings.unixSettings import UnixSettings

uae4armPath="/recalbox/share/emulateurs/amiga/uae4arm"
mountPoint="/tmp/amiga"
mountPointWHDL="/tmp/amiga/WHDL"
biosPath="/recalbox/share/bios/"
whdFilespath=biosPath+"amiga/whdl"

def generateWHDL(fullName,romFolder,gameName,amigaHardware,controller) :
    print("execute WHDLoad : <%s>" % os.path.join(romFolder,gameName))

    amiberryConfig.initMountpoint(mountPoint,uae4armPath)
    os.makedirs(mountPointWHDL)

    # ------------ copy WHDL structure Files ------------
    print("Copy WHDL bootstrap files from %s to %s" %(whdFilespath,mountPointWHDL))
    # TODO REDO IN PYTHON (not easily done)
    os.popen('cp -R '+whdFilespath+'/* '+mountPointWHDL)
    
    # ---- copy BIOS as equivalent into WHDL structure ----
    whdlKickstarts = os.path.join(mountPointWHDL,"Devs","Kickstarts")
    print(whdlKickstarts)
    shutil.copy2(os.path.join(biosPath,"kick13.rom"),os.path.join(whdlKickstarts,"kick33180.A500"))
    shutil.copy2(os.path.join(biosPath,"kick13.rom"),os.path.join(whdlKickstarts,"kick33192.A500"))
    shutil.copy2(os.path.join(biosPath,"kick13.rom"),os.path.join(whdlKickstarts,"kick34005.A500"))
    # shutil.copy2(os.path.join(biosPath,"kick20.rom"),os.path.join(whdlKickstart,))
    shutil.copy2(os.path.join(biosPath,"kick31.rom"),os.path.join(whdlKickstarts,"kick40068.A1200"))
    
    # ------------ copy game folder & uae ------------
    print("Copy game folder and uae %s" % os.path.join(romFolder,gameName))
    # TODO REDO IN PYTHON (not easily done)
    os.popen('cp -R "'+os.path.join(romFolder,gameName)+'/"* '+mountPointWHDL)
    shutil.copy2(os.path.join(romFolder,gameName+".uae"),os.path.join(mountPointWHDL,"uaeconfig.uae"))
    
    # ------------ Complete UAE ----------------
    uaeConfig = os.path.join(mountPointWHDL,"uaeconfig.uae")
    
    fUaeConfig = UnixSettings(uaeConfig, separator='', defaultComment=';')
    uaeConfigIsEmpty = os.path.getsize(uaeConfig) == 0
    
    # Needed or too speedy
    amiberryConfig.generateConfType(fUaeConfig)
    #Allow custom controllers conf in file
    if uaeConfigIsEmpty or not ';controls' in open(uaeConfig).read() :
        amiberryController.generateControllerConf(fUaeConfig)
        
    amiberryController.generateSpecialKeys(fUaeConfig,controller)
    amiberryConfig.generateGUIConf(fUaeConfig,'false')
    amiberryConfig.generateKickstartPathWHDL(fUaeConfig,amigaHardware)
    #Allow custom hardware conf in file
    if uaeConfigIsEmpty or not ';hardware' in open(uaeConfig).read() : 
        amiberryConfig.generateHardwareConf(fUaeConfig,amigaHardware)
    # Add Z3 Mem to load whole game in memory
    amiberryConfig.generateZ3Mem(fUaeConfig)
    amiberryConfig.generateGraphicConf(fUaeConfig)
    amiberryConfig.generateSoundConf(fUaeConfig)
    generateHardDriveConf(fUaeConfig)
    
    # ------------ Create StartupSequence with right slave files ------------
    fStartupSeq = open(os.path.join(mountPointWHDL,"S","Startup-Sequence"),"a+")
    try :
        slaveFiles = [filename for filename in os.listdir(mountPointWHDL) if filename.endswith(".Slave") or filename.endswith(".slave")]
        print(slaveFiles)
        if len(slaveFiles)==0 :
            sys.exit("This is not a valid WHD game")
        
        for slaveFile in slaveFiles :
            print("Using slave file %s" %slaveFile)
            fStartupSeq.write("WHDload "+slaveFile+" Preload\n")
            
        fStartupSeq.write("exitemu\n")
    finally :
        fStartupSeq.close()
        
    # TODO Tweak uae file
    
def generateHardDriveConf(fUaeConfig) :
    fUaeConfig.save("rtg_nocustom","true")
    fUaeConfig.save("filesystem2","rw,DH0:DH0:"+mountPointWHDL+"/,0")
    fUaeConfig.save("uaehf0","dir,rw,DH0:DH0:"+mountPointWHDL+"/,0")
    
def handleBackup(fullName,romFolder,gameName,amigaHardware) :
    # ------------ WHDL structure Files before backup of backups ------------
    shutil.rmtree(os.path.join(mountPointWHDL,'S'))
    shutil.rmtree(os.path.join(mountPointWHDL,'C'))
    shutil.rmtree(os.path.join(mountPointWHDL,'Devs'))
    os.remove(os.path.join(mountPointWHDL,"uaeconfig.uae"))
    
    # ------------ detect changes in remaining games files for backuping saves ------------
    print("Backup changed files from %s to %s" %(mountPointWHDL,os.path.join(romFolder,gameName)))
    backupDir(mountPointWHDL,os.path.join(romFolder,gameName))

def backupDir(source,target) :
    # print("backup dir <%s> <%s>" %(source, target))
    for f in os.listdir(source) :
        filePath = os.path.join(source,f)
        # print ("f : %s %s" %(source,f))
        if os.path.isdir(filePath) :
            backupDir(filePath,os.path.join(target,f))
        else :
            if not os.path.exists(os.path.join(target,f)) :
                print ("new file : %s backup %s -> %s" %(f,source,target))                
                if os.path.isdir(os.path.join(source,f)) :
                    # TODO REDO IN PYTHON (not easily done)
                    os.popen('cp -R "'+os.path.join(source,f)+'/"* "'+target+'"')
                else :
                    shutil.copy2(os.path.join(source,f),target)
			
            else :
                sourceCRC32 = CRC32_from_file(os.path.join(source,f))
                targetCRC32 = CRC32_from_file(os.path.join(target,f))
                if not sourceCRC32 == targetCRC32 :
                    print ("changed file : %s backup %s -> %s" %(f,source,target))
                    shutil.copy2(os.path.join(source,f),target)

def CRC32_from_file(filename):
    buf = open(filename,'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf
   