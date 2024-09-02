#!/bin/bash
cd server

> /src/log/output.log

# サーバーがすでに起動しているか確認
if screen -list | grep -q "papermc_server"; then
    echo "Server is already running in a screen session 'papermc_server'!"
    exit 1
fi

# サーバーを新しい screen セッションで起動
screen -L -Logfile /src/log/output.log -dmS papermc_server bash -c "java -Xms4096M -Xmx4096M --add-modules=jdk.incubator.vector -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -jar paper.jar --nogui"
echo "Server started in screen session 'papermc_server'."
