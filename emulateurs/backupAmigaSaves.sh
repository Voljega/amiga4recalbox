scriptPath="/emulateurs"
mountPointDir=$1
gameDir=$2
echo "backup_saves from $mountPointDir to $gameDir"
cd $mountPointDir
for fileMountPoint in `ls`
do
	echo "Treating $fileMountPoint in $mountPointDir"	
	if [ -d "$gameDir/$fileMountPoint" ]; then
		echo "$fileMountPoint is a directory, launch backup_saves from $mountPointDir/$fileMountPoint to $gameDir/$fileMountPoint"
		$scriptPath/backupAmigaSaves.sh $mountPointDir/$fileMountPoint $gameDir/$fileMountPoint
	else
		if [ ! -f "$gameDir/$fileMountPoint" ]; then
			echo "$fileMountPoint is a new save, backup it from $mountPointDir to $gameDir"
			cp -R $mountPointDir/$fileMountPoint $gameDir
		else
			echo "$fileMountPoint is found in $gameDir"			
			cd $mountPointDir						
			md5MountPointFile=`md5sum $fileMountPoint | awk '{print $1}'`
			#echo "MD5sum of $fileMountPoint in $mountPointDir : $md5MountPointFile"
			cd $gameDir						
			md5GameDirFile=`md5sum $fileMountPoint | awk '{print $1}'`
			#echo "MD5sum of $fileMountPoint in $gameDir : $md5GameDirFile"
			if [ "$md5MountPointFile" == "$md5GameDirFile" ];
			then
				echo "$fileMountPoint hasn't changed"
			else
				echo "$fileMountPoint has changed copy to $gameDir"
				cp -R $mountPointDir/$fileMountPoint $gameDir				
			fi			
		fi	
	fi
done
