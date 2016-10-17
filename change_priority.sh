#!/bin/bash
echo "Enter the PID"
read pid
if [ -e /proc/$pid ]; then
  echo "Enter a valid NICE value (between -20 and 19 for root user and 0 to 19 for non root users): "
  read nice_value
  if [[ $UID -ne 0 && $nice_value -lt "0" ]]; then
    echo "Only Root can use negative NICE value. Terminating.."
    exit 1
  fi
  if [ $nice_value -gt "-20" -a $nice_value -lt "19" ]; then
    echo "Changing priority scheduling"
    chrt -r -p $nice_value $pid
  else
    while [ 1 ]; do
      echo "Invalid NICE value."
      echo "Enter a valid NICE value (between -20 and 19 for root user and 0 to 19 for non root users): "
      read nice_value
      if [ $nice_value -gt "-20" -a $nice_value -lt "19" ]; then
        break
      fi
    done
    echo "Changing priority scheduling"
    chrt -r -p $nice_value $pid
  fi
else
  echo "Invalid PID"
fi
