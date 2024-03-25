container_id=$(docker run -d -p 5901:5901 --security-opt seccomp=unconfined quay.io/consideratio/test:turbo vncserver -xstartup /opt/install/jupyter_remote_desktop_proxy/share/xstartup -verbose -fg -geometry 1680x1050 -SecurityTypes None -rfbport 5901)
sleep 1

timeout --preserve-status 1 nc -v localhost 5901 2>&1 | \
  grep --quiet RFB && echo "Passed test" || { echo "Failed test" && TEST_OK=false; }

docker stop $container_id > /dev/null
if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi
