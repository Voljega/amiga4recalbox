# Custom Amiga Emulation for Recalbox

For Raspberry Pi 0,1,2 and 3
Compatible with ADF and WHD games
Using Midwan's amiberry 2.1 for RPI https://github.com/midwan/amiberry


Installation and update from previous versions
----------------------------------------------

- Just copy the installAmiga folder into `/recalbox/share`
- Then connect in SSH (through Putty or your prefered tool) and go to the folder `cd /recalbox/share/installAmiga`
- Launch the script with `./installAmiga.sh`, press Enter when needed and choose your Pi version when prompted
- Any modification to recalbox files or folders is backed-up so you can retrieve that if something goes wrong

- To play, you'll then to need search the net for BIOS files for Amiga (also known as kickstarts) and copy them to the `/recalbox/share/bios` folder after renaming them.
You may only need some of them if you don't want to use all systems

| MD5   | name to use   | for system   |
| ---   | ---   | ---   |
| 82a21c1890cae844b3df741f2762d48d    | kick13.rom      | ADF on Amiga 600   |
| dc10d7bdd1b6f450773dfb558477c230    | kick20.rom      | WHDL on Amiga 600   |
| 646773759326fbac3b2311fd8c8793ee    | kick31.rom      | ADF & WHDL on Amiga 1200   |
| 5f8924d013dd57a89cf349f4cdedc6b1    | kick31CD32.rom      | Amiga CD32   |
| bb72565701b1b6faece07d68ea5da639    | CD32ext.rom      | Amiga CD32   |
| 31e5bd652a7b4f2a818cd7d11a43b8bf    | cd32.nvr      | Amiga CD32   |

Usage
-------
- Use the 600 system for well for amiga 600 and the 1200 for amiga 1200, ADF are very touchy regarding that
- Keyboard and mouse are mandatory as many amiga games need custom key strokes to launch games
- Your keyboard will need to be configured as US in `recalbox.conf` for some games to launch if you use an azerty keyboard, quitting the emulator will be done through ctrl and a
- Enter GUI : ctrl or Start (Select for CD32)
- Quit game : ctrl and q or Hotkey

ADF games
---------
Just copy them to your amiga roms folder. Multi disks are automically loaded up to 4 for games using the standard naming "(Disk 1 of X)".

WHD games
------------------------
- Unzip them, delete the `.info` file at the same level than the folder, and copy only the folder to your roms folder (you can use subfolders i.e. `/recalbox/share/roms/amiga600/ShootEmUp)`
- You'll need a custom `.uae` file at the same level than the folder with the same name, two solutions :
- Copy the right one manually from `/recalbox/share/emulateurs` and rename it like your whdl game folder (keep the `.uae` extension)
- or generate then with :
- `genUAE.sh /recalbox/share/roms/amiga600 600` will generate an Amiga500 uae for every folder in the amiga600 roms folders
- `genUAE.sh /recalbox/share/roms/amiga1200 1200` will generate an Amiga1200 uae for every folder in the amiga1200 roms folders

KNOWN BUGS
------------
- WHD games using several slaves can have intros shown after game itself
- CD32 controller mapping ig buggy and only works fine on Xbox360 controllers

