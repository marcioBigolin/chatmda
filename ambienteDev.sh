#!/bin/sh

if [ "$(docker ps -a | grep chatmda)" ]; then
    echo "Container exists"
    docker start chatmda
else
    echo "Container does not exist! Creating ..."
    docker run -itd --network moodle-data-importer_mdinet --name chatmda -v $PWD:/app -p 8502:8501 gtechedu/streamlit  streamlit run chat.py 
fi