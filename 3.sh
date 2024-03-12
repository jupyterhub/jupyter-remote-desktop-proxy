container_id=$(docker run -d -p 0.0.0.0:8888:8888 -e JUPYTER_TOKEN=secret quay.io/consideratio/test:turbo)
sleep 5

curl --silent --fail 'http://127.0.0.1:8888/desktop/?token=secret' | grep --quiet 'Jupyter Remote Desktop Proxy' && echo "Passed get index.html test" || { echo "Failed" && TEST_OK=false; }
curl --silent --fail 'http://127.0.0.1:8888/desktop/static/dist/viewer.js?token=secret' > /dev/null && echo "Passed get viewer.js test" || { echo "Failed" && TEST_OK=false; }

websocat --binary --one-message --exit-on-eof 'ws://127.0.0.1:8888/desktop-websockify/?token=secret' | \
  grep --quiet RFB && echo "Passed initial websocket test" || { \
    echo "Failed initial websocket test" && sleep 3 && websocat --binary --one-message --exit-on-eof 'ws://127.0.0.1:8888/desktop-websockify/?token=secret' | grep --quiet RFB && echo "Passed second websocket test" || { echo "Failed second websocket test" && TEST_OK=false; } \
  }

echo "netstat inside container"
docker exec $container_id netstat -na --tcp | grep -E "(:5901|:5902)"
echo "netstat outside container"
netstat -na --tcp | grep -E "(:5901|:5902)"

timeout 5 docker stop $container_id > /dev/null && echo "Passed SIGTERM test" || { echo "Failed" && TEST_OK=false; }

if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi