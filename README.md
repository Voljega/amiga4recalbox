##Custom Amiga Emulation for Recalbox

Compatible with ADF, WHD folders, and TinyLauncher

Using ChiPs UAE4ARM v0.4 for RPI https://github.com/Chips-fr/uae4arm-rpi

Installation
--------------
- copy /emulateurs to you root directory
- give chmod 777 to every script files in /emulateurs
- verify that /emulateurs/amiga/uae4arm/uae4arm has 777 rights
- mkdir ram at root directory (this will be used by the script has a ram drive)
- copy /amiga contents to your /recalbox/share/roms/amiga and give 777 rights to TinyLauncher3 dir recursively
- integration with EmulationStation coming soon (but it's pretty easy to do, just modify es_systems.cfg to add amiga conf)

Usage
-------
- /emulateurs/amigascript.sh is the main script used for launching games in every format
- /emulateurs/genUae.sh is used to generate uae files for your WHD folders
- DO NOT USE MANUALLY THE OTHERS SCRIPTS, there are for internal usage by amigascript.sh only
- emulator can be quit with either the key shown at the beginning or stroke ctrl and select 'Quit' / press Q
- keyboard and mouse are mandatory as many amiga games need custom key strokes to launch games
- games are launched by /emulateurs/amiga/uae4arm

ADF games
---------
just copy them to your amiga roms folder, if the game uses several ADF, make sure that the different adfs have the same name except for the number at the end, you have to rename it if the last character isn't the number of the disk (ie if your name is ADF (Disk 1 of 2).adf rename it to ADF1.df or ADF Disk1, spaces are usable)

WHD games in direct mode
------------------------
- unzip them, delete the .info file at the same level than the folder, copy to your roms folder or subfolder
- you'll need a custom .uae file at the same level than the folder with the same name, you can either grab one from our pack (coming soon) or generate one (genUAE.sh /recalbox/share/roms/amiga will generate an uae for every folder in the amiga roms folders, you can off course use subfolders), you can also simply copy and rename one of the sample whd uae file from /emulateurs

WHD games with TinyLauncher
---------------------------
- unzip them, delete the .info file at the same level than the folder
- copy the game folder to /recalbox/share/roms/amiga/TinyLauncher3/GAMES
- launch TinyLauncher by using TinyLauncher.uae, click on ESC, then F1, let computation ends then ESC again, GAMES and select your game
 
KNOWN BUGS
------------
- Launching a SampleWHDGame.uae with no folder at the same level with name 'SampleWHDGame' will cause the emulator to crash and force you to reboot your recalbox
- WHD games using several slaves can have intros shown after game itself
- aspect ratio and image centering : you'll have to modify your uaes manually for the moment, for parameters force_aspectratio use true if you're in widescreen (16/9) or false in 4/3, next two parameters for centering should be put to simple

COMING SOON
-------------
- HD format games integration
- bugs correction
- custom uae packs for most well known games
- unique key configuration for quitting game (if possible)
- doc for ES integration
