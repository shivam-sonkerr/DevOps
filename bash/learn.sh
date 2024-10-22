#!/bin/bash

a=10
b=20

if [ $a -lt $b ]
then
   echo "a is less than b"
fi


c=$((a*b*a*b))
echo "Value of c is $c "
d=$((a*b*b))
echo "Value of d is $d"
echo $d
if [ $c -lt $d ]
then
   echo "c is less than d"
 else
   echo "c is greater than d"
fi
