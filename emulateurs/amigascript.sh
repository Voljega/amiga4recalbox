#!/bin/bash
#script constants
mountPoint="/ram"
# GAME directory contains necessary files/dir C S and Devs except Startup-Sequence
osFilespath="/emulateurs/GAME"
uae4armPath="/emulateurs/amiga/uae4arm"
scriptPath="/emulateurs"

#protection against nonsense
if [[ -z "$1" ]]; then
	echo "Please execute this script on full path to an uae or adf like /recalbox/share/roms/amiga/gamename.uae"
	echo "For uae file, the game folder should be named exactly alike"
	echo "and be in the same folder : /recalbox/share/roms/amiga/gamename"
	exit
fi

if [ -d "$1" ]; then
	echo "Please execute this script on full path to an uae or adf like /recalbox/share/roms/amiga/gamename.uae"
	echo "For uae file, the game folder should be named exactly alike"
	echo "and be in the same folder : /recalbox/share/roms/amiga/gamename"
	exit
fi

#command params
uaeName=`basename $1`
romFolder=`dirname $1`
le=`expr index "$uaeName" .`
romType=`expr substr "$uaeName" "$le" 4`
let "le = le - 1"
gameName=`expr substr "$uaeName" 1 "$le"`
echo "Launching game $gameName of type $romType from $romFolder"

if [ "$gameName" == "TinyLauncher" ]; 
then
	cd $uae4armPath
	echo "execute TinyLauncher : $uae4armPath/uae4arm on $romFolder/$uaeName"
	./uae4arm
	exit
fi

if	[ "$romType" == ".adf" ]; 
then
	cd $uae4armPath
	echo "execute ADF : $uae4armPath/uae4arm on $romFolder/$uaeName"
	$scriptPath/adflauncher.sh $1	
	exit
fi

echo "execute WHDLoad on $romFolder/$uaeName"
#mounting 24M ram on $mountpoint  
echo "Mounting 24M ram on $mountPoint"
mount -t tmpfs -o size=24M tmpfs $mountPoint

#copy Amiga OS Files
echo "Copy Amiga OS files from $osFilespath to $mountPoint"
cp -R $osFilespath/* $mountPoint

# copy game files & folder
cd $romFolder/$gameName
for fichier in `ls`
do
	echo "Copy Game File $fichier from $romFolder to $mountPoint"
	cp -R $fichier $mountPoint
done
cd $romFolder
echo "Copy $uaeName from $romFolder to $mountPoint"
cp $uaeName $mountPoint

#Modify StartupSequence with right slave file
cd $mountPoint
slaveFile=`ls *.slave`
if [ -z "$slaveFile" ]; then
    echo "slaveFile .slave does not exist, trying .Slave"
	slaveFile=`ls *.Slave`
fi

echo "use slaveFile $slaveFile"
cd S
touch Startup-Sequence
echo "WHDload $slaveFile Preload" >> Startup-Sequence
echo "exitemu" >> Startup-Sequence

# execute uae4arm
cd $uae4armPath
echo "execute $uae4armPath/uae4arm on $mountPoint/$uaeName"
/recalbox/scripts/runcommand.sh 4 "$uae4armPath/uae4arm -f $mountPoint/$uaeName"

cd $mountPoint
# clean Amiga OS Files before backup of backups
rm -rf S
rm -rf C
rm -rf Devs
rm $uaeName

# remaining games files used to detect saves to backup
$scriptPath/backupAmigaSaves.sh $mountPoint $romFolder/$gameName

# unmount with -l to avoid resource busy
umount -l $mountPoint