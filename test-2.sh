container_id=$(docker run -d -p 5901:5901 quay.io/consideratio/test:tiger websockify --verbose --log-file=/tmp/websockify.log --heartbeat=30 5901 -- vncserver -xstartup /opt/install/jupyter_remote_desktop_proxy/share/xstartup -verbose -fg -geometry 1680x1050 -SecurityTypes None -rfbport 5901)
sleep 1

docker exec $container_id bash -c 'websocat --no-async-stdio --binary --one-message --exit-on-eof "ws://localhost:5901/"' 2>&1 | tee output-inside.txt
cat output-inside.txt  | grep --quiet RFB && echo "Passed inside test"  || { echo "Failed inside test" && TEST_OK=false; }

websocat --no-async-stdio --binary --one-message --exit-on-eof "ws://localhost:5901/" 2>&1 | tee output-outside.txt
cat output-outside.txt | grep --quiet RFB && echo "Passed outside test" || { echo "Failed outside test" && TEST_OK=false; }

docker exec $container_id bash -c "cat /tmp/websockify.log"
docker exec $container_id bash -c "cat ~/.vnc/*.log"

docker stop $container_id > /dev/null
if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi
