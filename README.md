# Custom Amiga Emulation for Recalbox

THIS IS NOW INTEGRATED IN RECALBOX, PLEASE DON'T USE THIS VERSION ANYMORE

Code is kept here for documentation purposes

For Raspberry Pi 1,2 or 3

Compatible with ADF and WHD games

Using Midwan's amiberry 2.1 for RPI https://github.com/midwan/amiberry

For Recalbox v17.12.02


Installation and update from previous versions
----------------------------------------------

- Just copy the installAmiga folder into `/recalbox/share`
- Then connect in SSH (through Putty or your prefered tool) and go to the folder `cd /recalbox/share/installAmiga`
- Give 755 rights to the script : `chmod 755 installAmiga.sh`
- Launch the script with `./installAmiga.sh`, press Enter when needed and choose your Pi version when prompted
- Any modification to recalbox files or folders is backed-up so you can retrieve that if something goes wrong
- After installation and reboot are completed, you can delete the installAmiga folder

- To play, you'll then to need search the net for BIOS files for Amiga (also known as kickstarts) and copy them to the `/recalbox/share/bios` folder after renaming them.
You may only need some of them if you don't want to use all systems

| MD5   | name to use   | for system   |
| ---   | ---   | ---   |
| 82a21c1890cae844b3df741f2762d48d    | kick13.rom      | ADF on Amiga 600   |
| dc10d7bdd1b6f450773dfb558477c230    | kick20.rom      | WHDL on Amiga 600   |
| 646773759326fbac3b2311fd8c8793ee    | kick31.rom      | ADF & WHDL on Amiga 1200   |
| 5f8924d013dd57a89cf349f4cdedc6b1    | kick31CD32.rom      | Amiga CD32   |
| bb72565701b1b6faece07d68ea5da639    | CD32ext.rom      | Amiga CD32   |

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
##### Installation :

Unzip them, delete the `.info` file at the same level than the folder, and copy only the folder to your roms folder (you can use subfolders i.e. `/recalbox/share/roms/amiga1200/ShootEmUp)`

##### Usage :
You'll need an `.uae` file at the same level than the folder with the same name, two solutions :
- Create an empty one with same name as the folder
- Or use a custom one wich will allow you to tweak configuration of the emulator (see next paragraph)

**By default I recommend using amiga1200 folder for any WHDL game, if some of them are too fast, you can try them in amiga600 folder**

WHD games tweaking
------------------
### .uae file tweaking
In the uae file, you can define `;hardware`, `;controls` and `;graphics` blocks to replace the standard configuration of the emulator

This can allow you to play with two joysticks for instance, use very specific hardware configuration for some games that are a little special, or define a custom resolution

You can also erase eveything in the uae file and default emulator configuration will be used

Examples of custom uae files (using default configuration which you can change and tweak like you want) can be found in `/recalbox/share/emulateurs` :
 
Copy the one (corresponding to the amiga model you wan to use) next to your whdl game folder and rename it like your whdl game folder (keep the `.uae` extension)

You can also automatically generate them for all whdl games of your roms folder (up to one level of subfolders):
- `genUAE.sh /recalbox/share/roms/amiga600 600` will generate an Amiga500 uae for every folder in the amiga600 roms folders
- `genUAE.sh /recalbox/share/roms/amiga1200 1200` will generate an Amiga1200 uae for every folder in the amiga1200 roms folders

**Each custom configuration parts of your .uae file will only be used if it starts with the right block name : `;hardware`, `;controls` or `;graphics`**

### Startup-sequence tweaking (for experts only)
Standard generated launch sequence for WHDL games is `WHDload game.slave Preload` (in `WHDL/S/Startup-Sequence`)

But some few WHDL games (like History Line : 1914-1918 ) may require additionnal parameters on launch or they simply crash

You can add a second file (totally optional) to your setup to use those parameters, so you will have if we take History Line as example :
- HistoryLine (folder of the WHDL game)
- HistoryLine.uae (which can be empty or customized)
- HistoryLine.whdl (optional, containing additional parameters here `CUSTOM1=1`)

The game will then launch.

Here's a little list of games requiring those extra parameters.

| Game   | extra parameter(s)   |
| ---   | ---   |
| HistoryLine 1914-1918    | `CUSTOM1=1` for intro, `CUSTOM1=2` for game    |
| The Settlers / Die Siedlers    | `CUSTOM1=1` skips intro    |


KNOWN BUGS
------------
- WHD games using several slaves can have intros shown after game itself
- CD32 controller mapping ig buggy and only works fine on Xbox360 controllers

