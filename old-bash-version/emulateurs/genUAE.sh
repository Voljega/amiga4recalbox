#!/bin/bash
stdUae1200="/recalbox/share/emulateurs/standard_forceratio_1200.uae"
stdUae600="/recalbox/share/emulateurs/standard_forceratio_600.uae"
romFolder=$1
amigaHardware=$2
cd $romFolder
find . -maxdepth 1 -type d ! -wholename "./downloaded_images" ! -wholename "." | while read fileFolder ; do
	echo "$fileFolder is a directory"
	uaeFile="$fileFolder.uae"
	if [ ! -f "$romFolder/$uaeFile" ]; then
			echo "$uaeFile doesn't exist, creating it"
			
			if [ "$amigaHardware" == "1200" ]; then
				cp $stdUae1200 "$romFolder/$uaeFile"
			else
				cp $stdUae600 "$romFolder/$uaeFile"
			fi
	fi
done
