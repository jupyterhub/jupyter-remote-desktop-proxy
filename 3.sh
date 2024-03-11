container_id=$(docker run -d -p 8888:8888 --security-opt seccomp=unconfined -e JUPYTER_TOKEN=secret quay.io/consideratio/test:turbo)
sleep 5

echo "::group::Testing /desktop/ to return rendered index.html template"
curl --silent --fail 'http://localhost:8888/desktop/?token=secret' | grep --quiet 'Jupyter Remote Desktop Proxy' && echo "Passed" || { echo "Failed" && TEST_OK=false; }
echo "::endgroup::"

echo "::group::Testing /desktop/ to provide pre-built viewer.js"
curl --silent --fail 'http://localhost:8888/desktop/static/dist/viewer.js?token=secret' > /dev/null && echo "Passed" || { echo "Failed" && TEST_OK=false; }
echo "::endgroup::"

echo "::group::Testing /desktop-websockify/ to return a vncserver typical response, accepting one initial test failure"
websocat --no-async-stdio --binary --one-message --exit-on-eof 'ws://localhost:8888/desktop-websockify/?token=secret' | grep --quiet RFB && echo "Passed initial websocket test" || { \
    echo "Failed initial websocket test" && sleep 3 && websocat -vv --no-async-stdio --binary --one-message --exit-on-eof 'ws://localhost:8888/desktop-websockify/?token=secret' | tee /dev/tty | grep --quiet RFB && echo "Passed second websocket test" || { echo "Failed second websocket test" && TEST_OK=false; } \
}
echo "::endgroup::"

# echo "::group::jupyter_server logs"
# docker logs $container_id
# echo "::endgroup::"

# echo "::group::websockify logs"
# docker exec $container_id bash -c "cat /tmp/websockify.log"
# echo "::endgroup::"

# echo "::group::vncserver logs"
# docker exec $container_id bash -c "cat ~/.vnc/*.log"
# echo "::endgroup::"

echo "::group::Testing container's ability to terminate via SIGTERM"
timeout 5 docker stop $container_id > /dev/null && echo "Passed" || { echo "Failed" && TEST_OK=false; }
echo "::endgroup::"

if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi