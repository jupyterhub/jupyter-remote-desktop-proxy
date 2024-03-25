container_id=$(docker run -d -p 5901:5901 quay.io/consideratio/test:turbo websockify --verbose --log-file=/tmp/websockify.log --heartbeat=30 5901 -- vncserver -xstartup /opt/install/jupyter_remote_desktop_proxy/share/xstartup -verbose -fg -geometry 1680x1050 -SecurityTypes None -rfbport 5901)
sleep 1

websocat --binary --one-message --exit-on-eof "ws://localhost:5901/" 2>&1 | \
  grep --quiet RFB && echo "Passed test" || { echo "Failed test" && TEST_OK=false; }

docker stop $container_id > /dev/null
if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi
