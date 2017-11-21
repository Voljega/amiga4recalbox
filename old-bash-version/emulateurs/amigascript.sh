#!/bin/bash
#script constants
mountPoint="/recalbox/share/ram"
# GAME directory contains necessary files/dir C S and Devs except Startup-Sequence
osFilespath="/recalbox/share/emulateurs/GAME"
uae4armPath="/recalbox/share/emulateurs/amiga/uae4arm"
scriptPath="/recalbox/share/emulateurs"
amigaHardware="$2"

#------------ CHECK entry params ------------
#protection against nonsense
if [ -z "$1" ] || [ -d "$1" ]; then
	echo "Please execute this script on full path to an uae or adf like /recalbox/share/roms/amiga/gamename.uae"
	echo "For uae file, the game folder should be named exactly alike"
	echo "and be in the same folder : /recalbox/share/roms/amiga/gamename"
	exit
fi

#
if [ "$amigaHardware" == "1200" ]; then
	echo "Amiga Hardware 1200"
else
	echo "Amiga Hardware 600"
fi

#command params
uaeName=`basename "$1"`
romFolder=`dirname "$1"`
romType="${uaeName##*.}"
gameName="${uaeName%.*}"

echo "Before test : $gameName of type $romType from $romFolder"
#detect bad parameters
if  [ -z "$uaeName" ] || [ -z "$romFolder" ] || [ -z "$gameName" ]; then
	echo "Please execute this script on full path to an existing uae or adf like /recalbox/share/roms/amiga/gamename.uae"
	echo "For uae file, the game folder should be named exactly alike"
	echo "and be in the same folder : /recalbox/share/roms/amiga/gamename"
	exit
fi

echo "Launching game $gameName of type $romType from $romFolder"

#------------ Launch Tiny Launcher ------------
if [ "$gameName" == "TinyLauncher" ]; 
then
	cd $uae4armPath
	echo "execute TinyLauncher : $uae4armPath/uae4arm on $romFolder/$uaeName"
	./uae4arm -f "$romFolder/$uaeName"
	exit
fi

#------------ Launch ADF ------------
if	[ "$romType" == "adf" ]; 
then
	if [ ! -f "$romFolder/$uaeName" ]; then
		echo "ADF file $romFolder/$uaeName doesn't exist"
		exit
	fi
	cd $uae4armPath
	echo "execute ADF : $uae4armPath/uae4arm on $romFolder/$uaeName"
	$scriptPath/adflauncher.sh "$1" "$romFolder" "$uaeName" "$amigaHardware"
	exit
fi

#------------ Launch WHD ------------
if [ ! -d "$romFolder/$gameName" ]; then
    echo "A WHD folder $romFolder/$gameName corresponding to your uae file $romFolder/$uaeName doesn't exist"
	exit
fi

echo "execute WHDLoad on $romFolder/$uaeName"
#mounting 24M ram on $mountpoint  
echo "Mounting 24M ram on $mountPoint"
mount -t tmpfs -o size=24M tmpfs $mountPoint

#------------ copy Amiga OS Files ------------
echo "Copy Amiga OS files from $osFilespath to $mountPoint"
cp -R $osFilespath/* $mountPoint

#------------ copy game files & folder ------------
cd "$romFolder/$gameName"
for fichier in `ls`
do
	echo "Copy Game File $fichier from $romFolder to $mountPoint"
	cp -R "$fichier" $mountPoint
done
cd "$romFolder"
echo "Copy $uaeName from $romFolder to $mountPoint"
cp "$uaeName" $mountPoint

#------------ Modify StartupSequence with right slave files ------------
cd $mountPoint
touch Startup-Sequence
slaveFiles=`ls *.slave`
if [ -z "$slaveFiles" ]; then
    echo "slaveFiles .slave does not exist, trying .Slave"
	slaveFiles=`ls *.Slave`
	if [ -z "$slaveFiles" ]; then
		echo "This is not a valid WHD game"
	else
		for slave in `ls *.Slave`
		do
			echo "use slaveFile $slave"
			echo "WHDload $slave Preload" >> Startup-Sequence
		done
	fi	
else	
	for slave in `ls *.slave`
	do
		echo "use slaveFile $slave"
		echo "WHDload $slave Preload" >> Startup-Sequence
	done
fi

echo "exitemu" >> Startup-Sequence
mv Startup-Sequence $mountPoint/S

#------------ execute uae4arm ------------
cd $uae4armPath
echo "execute $uae4armPath/uae4arm on $mountPoint/$uaeName"
./uae4arm -f "$mountPoint/$uaeName"

cd $mountPoint
#------------ clean Amiga OS Files before backup of backups ------------
rm -rf S
rm -rf C
rm -rf Devs
rm "$uaeName"

#------------ remaining games files used to detect saves to backup ------------
$scriptPath/backupAmigaSaves.sh $mountPoint "$romFolder/$gameName"

#------------ unmount with -l to avoid resource busy ------------
umount -l $mountPoint
