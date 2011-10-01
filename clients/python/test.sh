#!/bin/bash

for i in {1..20}
do
    echo $i | python client.py $i &
    sleep 0.2
done
