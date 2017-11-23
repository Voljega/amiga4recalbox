#!/bin/bash
supportVersion="17.11.10.2"
echo " "
echo "This script is going to install or update amiga on your recalbox, which should be in version $supportVersion"
echo "Please update your recalbox before using this script or wait for a new amiga4recalbox update if this is not the case"
echo "REMEMBER THIS IS EXPERIMENTAL, ALWAYS HAVE A BACKUP OF YOUR ROMS, BIOS, CUSTOM CONF, ETC"
echo "Press x to exit script and stop installation or any other key to continue"
read ok
if [ "$ok" == "x" ] || [ "$ok" == "X" ]; then
    echo "Installation cancelled by user"
    exit
fi
# ---- Passing in rw mode on partition /
echo "Mount / in rw"
mount -o remount,rw /
# ---- Move lib folder
echo "Copy /lib dir"
rsync -a /recalbox/share/installAmiga/lib/ /lib/
if [ ! -d "/recalbox/share/emulateurs/" ]; then
    mkdir /recalbox/share/emulateurs
fi
if [ -d "/recalbox/share/emulateurs/amiga" ]; then
    if [ -d "/recalbox/share/emulateurs/.amigabak" ]; then
        rm -rf "/recalbox/share/emulateurs/.amigabak"
    fi
    echo "Backup existing /recalbox/share/emulateurs/amiga to /recalbox/share/emulateurs/.amigabak"
    mv -f /recalbox/share/emulateurs/amiga /recalbox/share/emulateurs/.amigabak
fi
# ---- Binary and genUAE directory
echo "Copy emulateurs to /recalbox/share/"
rsync -a /recalbox/share/installAmiga/emulateurs/ /recalbox/share/emulateurs/
chmod 755 -R /recalbox/share/emulateurs/amiga
echo "Which Raspberry Pi are you using : 1,2 or 3 ?"
read piVersion
if  [ ! "$piVersion" == "0" ] && [ ! "$piVersion" == "1" ] && [ ! "$piVersion" == "2" ] && [ ! "$piVersion" == "3" ];
then
    echo "Version number must be 0,1,2 or 3, please re-enter :"
    read piVersion
fi
echo "Using Raspberry Pi $piVersion"
mv -f "/recalbox/share/emulateurs/amiga/uae4arm/amiberry-rpi$piVersion" "/recalbox/share/emulateurs/amiga/uae4arm/uae4arm"
# ---- Es_systems_cfg in share_init
echo "Customize /recalbox/share_init/system/.emulationstation/es_systems.cfg"
mv -f /recalbox/share_init/system/.emulationstation/es_systems.cfg /recalbox/share_init/system/.emulationstation/es_systems.bak
cp es_systems.cfg /recalbox/share_init/system/.emulationstation/es_systems.cfg
# ---- Configgen tweaking
echo "Modify configgen scripts"
if [ -f "/usr/lib/python2.7/site-packages/configgen/emulatorlauncher.bak" ]; then
    rm -f /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.bak
fi
mv -f /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.py /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.bak
if [ -f "/usr/lib/python2.7/site-packages/configgen/recalboxFiles.bak" ]; then
    rm -f /usr/lib/python2.7/site-packages/configgen/recalboxFiles.bak
fi
mv -f /usr/lib/python2.7/site-packages/configgen/recalboxFiles.py /usr/lib/python2.7/site-packages/configgen/recalboxFiles.bak
rsync -a /recalbox/share/installAmiga/configgen/ /usr/lib/python2.7/site-packages/configgen/
# ---- Generates bios and roms folders
echo "Create WHDL conf in /recalbox/share/bios/amiga"
if [ ! -d "/recalbox/share/bios/amiga" ]; then
    echo "Create /recalbox/share/bios/amiga"
    mkdir "/recalbox/share/bios/amiga"
fi
if [ -d "/recalbox/share/bios/amiga/whdl" ]; then
    if [ -d "/recalbox/share/bios/amiga/.whdlbak" ]; then
        rm -rf "/recalbox/share/bios/amiga/.whdlbak"        
    fi
    echo "Backup existing /recalbox/share/bios/amiga/whdl to /recalbox/share/bios/amiga/.whdlbak"
    mv -f /recalbox/share/bios/amiga/whdl /recalbox/share/bios/amiga/.whdlbak
fi
cp -R whdl /recalbox/share/bios/amiga
chmod 755 -R /recalbox/share/bios/amiga/whdl
if [ ! -d "/recalbox/share/roms/amiga600" ]; then
    echo "Create /recalbox/share/roms/amiga600"
    mkdir "/recalbox/share/roms/amiga600"
fi
if [ ! -d "/recalbox/share/roms/amiga1200" ]; then
    echo "Create /recalbox/share/roms/amiga1200"
    mkdir "/recalbox/share/roms/amiga1200"
fi
if [ ! -d "/recalbox/share/roms/amigacd32" ]; then
    echo "Create /recalbox/share/roms/amigacd32"
    mkdir "/recalbox/share/roms/amigacd32"
fi
# ---- Recompile emulatorlauncher.py
cd /usr/lib/python2.7/site-packages/configgen/
rm emulatorlauncher.pyc
python -m compileall emulatorlauncher.py
echo "Installation completed, your recalbox is now going to reboot"
echo "Press any key"
read reb
reboot

