#!/bin/bash
uae4armPath="/recalbox/share/emulateurs/amiga/uae4arm"
mountPoint="/recalbox/share/ram"

#mounting 24M ram on $mountpoint  
echo "Mounting 24M ram on $mountPoint for use of adf $1"
mount -t tmpfs -o size=24M tmpfs $mountPoint

#copy Amiga OS Files
echo "Copy uae4arm files to $mountPoint"
mkdir $mountPoint/uae4arm
cp -R $uae4armPath/* $mountPoint/uae4arm
cd $mountPoint/uae4arm/conf

# ----- CREATE adfdir.conf -----
# On créer un fichier au démarrage du script pour configurer uae4arm
touch raw.uae

#Configuration des contrôles
echo "config_version=2.8.1" >> raw.uae
echo "joyport0=mouse" >> raw.uae
echo "joyport0autofire=none" >> raw.uae
echo "joyport0mode=mouse" >> raw.uae
echo "joyportname0=MOUSE0" >> raw.uae
echo "joyport1=joy0" >> raw.uae
echo "joyport1autofire=normal" >> raw.uae
echo "joyport1mode=djoy" >> raw.uae
echo "joyportname1=JOY1" >> raw.uae

#On le complete avec l'autolauncher
echo "use_gui=no" >> raw.uae
echo "use_debugger=false" >> raw.uae
echo "kickstart_rom_file=$mountPoint/uae4arm/kickstarts/kick13.rom" >> raw.uae
echo "floppy0=$1" >> raw.uae

# On cherche si le jeu est sur plusieurs disquettes.
echo "floppy1=${1//Disk 1/Disk 2}" >> raw.uae
echo "floppy2=${1//Disk 1/Disk 3}" >> raw.uae
echo "floppy2type=0" >> raw.uae
echo "floppy3=${1//Disk 1/Disk 4}" >> raw.uae
echo "floppy3type=0" >> raw.uae
echo "nr_floppies=4" >> raw.uae

# On modifie optimise si c'est un jeu en AGA
echo "chipset=aga" >> raw.uae
echo "chipmem_size=4" >> raw.uae

# On optimise la résolution du script.
echo "gfx_width=640" >> raw.uae
echo "gfx_height=256" >> raw.uae
echo "gfx_correct_aspect=true" >> raw.uae
echo "gfx_center_horizontal=simple" >> raw.uae
echo "gfx_center_vertical=simple" >> raw.uae

#regenerate uaeconfig.uae
rm $mountPoint/uae4arm/conf/adfdir.conf
touch adfdir.conf
echo "path=$mountPoint/uae4arm/adf/" >> adfdir.conf
echo "config_path=$mountPoint/uae4arm/conf/" >> adfdir.conf
echo "rom_path=$mountPoint/uae4arm/kickstarts/" >> adfdir.conf
echo "ROMs=2" >> adfdir.conf
echo "ROMName=KS ROM v1.3 (A500,A1000,A2000)" >> adfdir.conf
echo "ROMPath=$mountPoint/uae4arm/kickstarts/kick13.rom" >> adfdir.conf
echo "ROMType=1" >> adfdir.conf
echo "ROMName=KS ROM v3.1 (A1200)" >> adfdir.conf
echo "ROMPath=$mountPoint/uae4arm/kickstarts/kick31.rom" >> adfdir.conf
echo "ROMType=1" >> adfdir.conf

# On place le fichier au bon endroit et on lance l'emulateur.
cd $mountPoint/uae4arm/
rm $mountPoint/uae4arm/conf/uaeconfig.uae
mv $mountPoint/uae4arm/conf/raw.uae $mountPoint/uae4arm/conf/uaeconfig.uae
./uae4arm

# unmount with -l to avoid resource busy
umount -l $mountPoint