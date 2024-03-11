# container_id=$(docker run -d -p 5901:5901 --security-opt seccomp=unconfined quay.io/consideratio/test:turbo websockify --verbose --log-file=/tmp/websockify.log --heartbeat=30 5901 -- vncserver -xstartup /opt/install/jupyter_remote_desktop_proxy/share/xstartup -verbose -fg -geometry 1680x1050 -SecurityTypes None -rfbport 5901)
container_id=$(docker run -d -p 5901:5901 -v $(pwd):/mnt/test --security-opt seccomp=unconfined quay.io/consideratio/test:turbo websockify --verbose --log-file=/tmp/websockify.log --heartbeat=30 5901 -- python /mnt/test/dummy-tcp-server.py)
sleep 3

# echo "::group::Installing websocat (inside container)"
# docker exec --user root $container_id bash -c '
#   wget -q https://github.com/vi/websocat/releases/download/v1.12.0/websocat.x86_64-unknown-linux-musl \
#     -O /usr/local/bin/websocat
#   chmod +x /usr/local/bin/websocat
# '
# echo "::endgroup::"

echo "::group::Testing websockify'ed vncserver with websocat (inside container)"
docker exec $container_id bash -c 'websocat --binary --one-message --exit-on-eof "ws://localhost:5901/"' 2>&1 | tee output-inside.txt
cat output-inside.txt  | grep --quiet RFB && echo "Passed inside test"  || { echo "Failed inside test" && TEST_OK=false; }
echo "::endgroup::"

echo "::group::Testing websockify'ed vncserver with websocat (outside container)"
websocat --binary --one-message --exit-on-eof "ws://localhost:5901/" 2>&1 | tee output-outside.txt
cat output-outside.txt | grep --quiet RFB && echo "Passed outside test" || { echo "Failed outside test" && TEST_OK=false; }
echo "::endgroup::"

# echo "::group::websockify logs"
# docker exec $container_id bash -c "cat /tmp/websockify.log"
# echo "::endgroup::"

# echo "::group::vncserver logs"
# docker exec $container_id bash -c "cat ~/.vnc/*.log"
# echo "::endgroup::"

docker stop $container_id > /dev/null
if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi