#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/status)
if [[ $? == "0" ]] ; then
	goecorrectionfactor=$goecorrectionfactorlp2
	goecorrectionfactor=$(echo "scale=0;$goecorrectionfactor * 100000 /1" |bc)
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		wattc=$((watt*$goecorrectionfactor/100000))
		wattc=$(echo "scale=0;$wattc" |bc)
		echo $wattc > /var/www/html/openWB/ramdisk/llaktuells1
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=0;$lla1 / 10" |bc)
	if [[ $lla1 =~ $re ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/llas11
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=0;$lla2 / 10" |bc)
	if [[ $lla2 =~ $re ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/llas12
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=0;$lla3 / 10" |bc)
	if [[ $lla3 =~ $re ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/llas13
	fi
	llv1=$(echo $output | jq -r '.nrg[0]')
	if [[ $llv1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llvs11
	fi
	llv2=$(echo $output | jq -r '.nrg[1]')
	if [[ $llv2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llvs12
	fi
	llv3=$(echo $output | jq -r '.nrg[2]')
	if [[ $llv3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llvs13
	fi
	llkwh=$(echo $output | jq -r '.eto')
	llkwh=$(echo "scale=3;$llkwh / 10" |bc)
    #simulation der Energiemenge während des ladens
	#wenn die Dateien noch nicht da sind, werden sie angelegt sobald das Auto nicht angesteckt ist.
	if [ -f "/var/www/html/openWB/ramdisk/goe2watt0neg" ]; then
		if [ -f "/var/www/html/openWB/ramdisk/goe2watt0pos" ]; then
			python /var/www/html/openWB/runs/simcount.py $wattc goe2 goe2poskwh goe2negkwh
		fi
	fi
	#car status 1 Ladestation bereit, kein Auto
	#car status 2 Auto lädt
	#car status 3 Warte auf Fahrzeug
	#car status 4 Ladung beendet, Fahrzeug verbunden
	car=$(echo $output | jq -r '.car')
	if [[ $goesimulationlp2 == "0" ]] ; then
		if [[ $llkwh =~ $rekwh ]] ; then
			echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs1
		fi
	else
		if [[ $car != "1" ]] ; then
			#der ausgelesene Zählerstand wird ignoriert und stattdessen die Leistung aufintegriert
			#Grund: der ausgelesene Zählerstand hat eine Auflösung von 1kWh -> zu ungenau in der Darstellung
			if [ -f "/var/www/html/openWB/ramdisk/goe2poskwh" ]; then
				simenergy=$(echo "scale=3; $(</var/www/html/openWB/ramdisk/goe2poskwh)/1000" | bc)
				echo $simenergy > /var/www/html/openWB/ramdisk/llkwhs1
			else
				echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs1
			fi
		fi
	fi
	if [[ $car == "1" ]] ; then
		echo 0 > /var/www/html/openWB/ramdisk/plugstats1
	else
		echo 1 > /var/www/html/openWB/ramdisk/plugstats1
	fi
	if [[ $car == "2" ]] ; then
		echo 1 > /var/www/html/openWB/ramdisk/chargestats1
	else
		echo 0 > /var/www/html/openWB/ramdisk/chargestats1
	fi
fi
