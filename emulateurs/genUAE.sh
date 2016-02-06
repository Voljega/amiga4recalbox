#!/bin/bash
stdUae="/emulateurs/standard_forceratio.uae"
romFolder=$1
cd $romFolder
for fileFolder in `ls`
do
	if [ -d "$romFolder/$fileFolder" ]; then
		echo "$fileFolder is a directory"
		uaeFile="$fileFolder.uae"
		if [ ! -f "$romFolder/$uaeFile" ]; then
			echo "$uaeFile doesn't exist, creating it"
			cp $stdUae $romFolder/$uaeFile
		fi
	fi
done
