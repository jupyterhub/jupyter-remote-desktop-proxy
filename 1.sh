# container_id=$(docker run -d -p 5901:5901 --security-opt seccomp=unconfined quay.io/consideratio/test:turbo vncserver -xstartup /opt/install/jupyter_remote_desktop_proxy/share/xstartup -verbose -fg -geometry 1680x1050 -SecurityTypes None -rfbport 5901)
container_id=$(docker run -d -p 0.0.0.0:5901:5901 -v $(pwd):/mnt/test quay.io/consideratio/test:turbo python /mnt/test/dummy-tcp-server.py)
sleep 3

# echo "::group::Installing netcat (inside container)"
# docker exec --user root $container_id bash -c '
#   apt update
#   apt install -y netcat net-tools
# '
# echo "::endgroup::"

docker exec $container_id bash -c 'timeout --preserve-status 1 nc -v 127.0.0.1 5901' 2>&1 | \
  grep --quiet RFB && echo "Passed inside test" || { echo "Failed inside test" && TEST_OK=false; }

timeout --preserve-status 1 nc -v 127.0.0.1 5901 2>&1 | \
  grep --quiet RFB && echo "Passed outside test" || { echo "Failed outside test" && TEST_OK=false; }

echo "netstat inside container"
docker exec $container_id netstat -na --tcp | grep -E "(:5901|:5902)"
echo "netstat outside container"
netstat -na --tcp | grep -E "(:5901|:5902)"

docker stop $container_id > /dev/null
if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi
