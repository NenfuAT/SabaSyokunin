#!/bin/bash

# ディレクトリが存在しない場合のみ作成
if [ ! -d "/src/server" ]; then
    mkdir -p /src/server
	echo "eula=true" > /src/server/eula.txt
fi

if [ ! -d "/src/log" ]; then
    mkdir -p /src/log
	echo > /src/log/output.log
fi

# サーバーディレクトリに移動
cd /src/server

# Download the latest version of the script
URL='https://api.papermc.io/v2/projects/paper'

# Get the latest version
VERSION=$(curl -X 'GET' $URL -H 'accept: application/json' | jq -r '.versions[-1]')
echo "Latest version: $VERSION"

# Get the latest build
BUILD=$(curl -X 'GET' $URL/versions/$VERSION -H 'accept: application/json' | jq -r '.builds[-1]')
echo "Latest build: $BUILD"

# Download the jar
curl -X 'GET' $URL/versions/$VERSION/builds/$BUILD/downloads/paper-$VERSION-$BUILD.jar -o paper.jar

