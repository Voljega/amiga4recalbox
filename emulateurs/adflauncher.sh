#!/bin/bash
uae4armPath="/recalbox/share/emulateurs/amiga/uae4arm"
mountPoint="/recalbox/share/ram"
fullName="$1"
romPath="$2"
uaeName="$3"
amigaHardware="$4"

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
#echo "pandora.joy_conf=0" >> raw.uae
#echo "pandora.joy_port=0" >> raw.uae
#echo "pandora.custom_dpad=1" >> raw.uae
#echo "pandora.button1=2" >> raw.uae
#echo "pandora.button2=1" >> raw.uae
echo "joyport0=mouse" >> raw.uae
echo "joyport0autofire=none" >> raw.uae
echo "joyport0mode=mouse" >> raw.uae
echo "joyportname0=MOUSE0" >> raw.uae
echo "joyport1=joy0" >> raw.uae
echo "joyport1autofire=normal" >> raw.uae
echo "joyport1mode=djoy" >> raw.uae
echo "joyportname1=JOY1" >> raw.uae

echo "use_gui=no" >> raw.uae
echo "use_debugger=false" >> raw.uae

if [ "$amigaHardware" == "1200" ]; then
	echo "Amiga Hardware 1200 AGA"
	echo "kickstart_rom_file=$mountPoint/uae4arm/kickstarts/kick31.rom" >> raw.uae
	# On configure en AGA
	echo "chipset=aga" >> raw.uae
	echo "chipmem_size=4" >> raw.uae
	echo "cpu_speed=max" >> raw.uae
	echo "cpu_type=68040" >> raw.uae
	echo "cpu_model=68040" >> raw.uae
	echo "fpu_model=68040" >> raw.uae
else
	echo "Amiga Hardware 600"
	echo "kickstart_rom_file=$mountPoint/uae4arm/kickstarts/kick13.rom" >> raw.uae
fi


#floppies management
strindex() { 
  x="${1%%$2*}"
  [[ "$x" = "$1" ]] && echo -1 || echo ${#x}
}

index=`strindex "$uaeName" "Disk 1"`
echo "Disk 1 $index"
nbDisks="0"
if [ "$index" == "-1" ]; then
	# Mono disk
	echo "floppy0=${1}" >> raw.uae
	echo "Added $1 as floppy0"
	echo "floppy0type=0" >> raw.uae
	let "nbDisks = nbDisks + 1"
	echo "nr_floppies=1" >> raw.uae
	echo "number of floppies 1"
else
	# Several disks
	let "index = index + 4"
	prefix=`expr substr "$uaeName" 1 "$index"`
	echo "prefix $prefix"
	find "$romPath" -name "$prefix*" | sort | while read i
	do
		echo "floppy$nbDisks=${i}" >> raw.uae
		echo "floppy${nbDisks}type=0" >> raw.uae
		echo "Added $i as floppy$nbDisks"
		let "nbDisks = nbDisks + 1"
		if [ "$nbDisks" -eq "4" ]; then
			break
		fi
	done
	nbFloppies=( $(find "$romPath" -name "$prefix*" | wc -l) )
	if [ "$nbFloppies" -gt "4" ]; then
		echo "nr_floppies=4" >> raw.uae
		echo "number of floppies 4"
	else
		
		echo "nr_floppies=$nbFloppies" >> raw.uae
		echo "number of floppies $nbFloppies"
	fi
	
fi

# On optimise la résolution du script.
echo "gfx_width=640" >> raw.uae
echo "gfx_height=256" >> raw.uae
echo "gfx_correct_aspect=true" >> raw.uae
echo "gfx_center_horizontal=simple" >> raw.uae
echo "gfx_center_vertical=simple" >> raw.uae

#regenerate adfdir.conf
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

