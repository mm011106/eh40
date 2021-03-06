#!/bin/bash
#
# setup internet connection by Soracom air SIM with MS-2372 USB dongle
#  2020/1/12 miyamoto
#
#  need I2C bus must be enabled:
#    raspi-config -> interface -> I2C
#
#  need pppconfig and python-smbus :
#    apt install pppconfig python-smbus

SCRIPT_DIR=$(cd $(dirname $0);pwd)
TIME_STAMP=`date +%Y%m%d%H%M%S`
#echo $TIME_STAMP
#echo $SCRIPT_DIR

echo "Start setting up files for connecting the net via Soracom Serivce..."

if [ ! `id -u -n` = 'root' ]; then
	echo "Please run as root....  "
	exit 1
fi

TARGET_DIR='/etc/ppp/peers'
if [ ! -e $TARGET_DIR/soracom_MS2372 ]; then
  echo "cp ./ppp/peers/soracom_MS2372 $TARGET_DIR"
  echo " -- peers config copied.. "
else
  echo " -- peers config already exists. nothing changed."
fi

TARGET_DIR='/etc/chatscripts'
if [ ! -e $TARGET_DIR/soracom_MS2372 ]; then
  echo "cp ./ppp/chatscript/soracom_MS2372 $TARGET_DIR"
  echo " -- chatscript config copied.."
else
  echo " -- chatscript config already exists. nothing changed."
fi

TARGET_DIR='/etc/ppp/resolv'
if [ ! -e $TARGET_DIR/soracom_MS2372 ]; then
  echo "cp ./ppp/resolv/soracom_MS2372 $TARGET_DIR"
  echo " -- resolv config copied.."
else
  echo " -- resolv config already exists. nothing changed."
fi

TARGET_DIR='/etc/udev/rules.d'
if [ ! -e $TARGET_DIR/40-MS2372.rules ]; then
  echo "cp ./ppp/40-MS2372.rules $TARGET_DIR"
  echo " -- udev rule copied.."
else
  echo " -- udev rule already exists. nothing changed."
fi

TARGET_DIR='/lib/systemd/system'

echo "Start detalogger service..."
if [ ! -e $TARGET_DIR/soracom.service ]; then
	echo "  found no Service file.  Generating file..."
  sed -e "s|##CURRENT_DIR##|$SCRIPT_DIR|g" ./soracom.service > $TARGET_DIR/soracom.service
fi
if [ ! `systemctl is-enabled soracom` = 'enabled' ]; then
  systemctl start soracom.service && systemctl enable soracom.service
	echo "... Started"
else
	echo "... The service is already enabled"
fi

echo "Start Shutdown Sw service..."
if [ ! -e $TARGET_DIR/shutdwnSwitch.service ]; then
  echo "  found no Service file.  Generating file..."
	sed -e "s|##CURRENT_DIR##|$SCRIPT_DIR|g" ./shutdwnSwitch.service > $TARGET_DIR/shutdwnSwitch.service
fi
if [ ! `systemctl is-enabled shutdwnSwitch` = 'enabled' ]; then
  systemctl start shutdwnSwitch.service && systemctl enable shutdwnSwitch.service
  echo "... Started"
else
  echo "... The service is already enabled"
fi

echo "Configure network interface..."
mv /etc/network/interfaces /etc/network/interfaces.BUP_$TIME_STAMP && cp ./ppp/network/interfaces /etc/network

echo "Stopping swap service..."
if [ ! `systemctl is-enabled dphys-swapfile` = 'disabled' ]; then
  systemctl stop dphys-swapfile.service && systemctl disable dphys-swapfile.service
fi
