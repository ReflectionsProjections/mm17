#!/bin/sh -e

protoc --java_out=../server/src/ --java_out=../client/coffee/src/ mm17.proto
