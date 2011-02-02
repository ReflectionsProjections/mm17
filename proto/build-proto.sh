#!/bin/sh -e

protoc --java_out=../server/src/ --java_out=../client/ mm17.proto
