#!/bin/bash

for i in {1..4}
do
    echo $i
    echo $i | python client.py $i &
    sleep 0.2
done
