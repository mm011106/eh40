#!/bin/bash

#pwd
SCRIPT_DIR=$(cd $(dirname $0);pwd)
TIME_STAMP=`date +%Y%m%d%H%M%S`
#echo $TIME_STAMP
#echo $SCRIPT_DIR
echo $1

echo $(id -u -n)

TARGET_DIR='/etc/ppp/peers'
if [ ! -e $TARGET_DIR/soracom_MS2372 ]; then
  if [ $1 != "test" ]; then
    cp ./ppp/peers/soracom_MS2372 $TARGET_DIR 
    echo " peers config copied.. "
  else
    echo "changing in $TARGET_DIR"
  fi

else
  echo " peers config already exists. nothing changed."
fi

TARGET_DIR='/etc/chatscripts'
if [ ! -e $TARGET_DIR/soracom_MS2372 ]; then
#  cp ./ppp/chatscript/soracom_MS2372 $TARGET_DIR
  echo " chatscript config copied.."
else
  echo " chatscript config already exists. nothing changed."
fi

TARGET_DIR='/etc/ppp/resolv'
if [ ! -e $TARGET_DIR/soracom_MS2372 ]; then
#  cp ./ppp/resolv/soracom_MS2372 $TARGET_DIR
  echo " resolv config copied.."
else
  echo " resolv config already exists. nothing changed."
fi

if [ ! -e /etc/udev/rules.d/40-MS2372.rules ]; then
#  cp ./ppp/40-MS2372.rules /etc/udev/rules.d
  echo " udev rule copied.."
else
  echo " udev rule already exists. nothing changed."
fi

sed -e "s|##CURRENT_DIR##|$SCRIPT_DIR|g" ./soracom.service   

#mv /etc/network/interfaces /etc/network/interfaces.BUP_$TIME_STAMP
#cp ./ppp/network/interfaces /etc/network

