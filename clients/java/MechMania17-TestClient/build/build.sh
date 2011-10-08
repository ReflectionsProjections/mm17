#!/bin/bash

echo "Making output directory..."
mkdir -p ../bin

echo "Building org.json library..."
javac -classpath ../bin ../src/org/json/JSONException.java ../src/org/json/JSONTokener.java ../src/org/json/JSONString.java ../src/org/json/JSONArray.java ../src/org/json/JSONObject.java -d ../bin

echo "Building test client..."
javac -classpath ../bin ../src/edu/uiuc/acm/mechmania/objects/Ship.java -d ../bin/
javac -classpath ../bin ../src/edu/uiuc/acm/mechmania/objects/Planet.java -d ../bin/
javac -classpath ../bin ../src/edu/uiuc/acm/mechmania/objects/Refinery.java -d ../bin/
javac -classpath ../bin ../src/edu/uiuc/acm/mechmania/objects/Base.java -d ../bin/

javac -classpath ../bin ../src/edu/uiuc/acm/mechmania/infotypes/*.java -d ../bin/
javac -classpath ../bin ../src/edu/uiuc/acm/mechmania/*.java -d ../bin/

echo "Build complete."
