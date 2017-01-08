#!/bin/bash
stdUae="/recalbox/share/emulateurs/standard_forceratio.uae"
romFolder=$1
cd $romFolder
find . -maxdepth 1 -type d | while read fileFolder ; do
	echo "$fileFolder is a directory"
	uaeFile="$fileFolder.uae"
	if [ ! -f "$romFolder/$uaeFile" ]; then
			echo "$uaeFile doesn't exist, creating it"
			cp $stdUae "$romFolder/$uaeFile"
	fi
done
