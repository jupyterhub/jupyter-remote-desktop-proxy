# container_id=$(docker run -it -d -p 5901:5901 -p 5901:5901/udp quay.io/consideratio/test:tiger vncserver -xstartup /opt/install/jupyter_remote_desktop_proxy/share/xstartup -verbose -fg -geometry 1680x1050 -SecurityTypes None)
container_id=$(docker run -it -d -p 5901:5901 -p 5901:5901/udp quay.io/consideratio/test:tiger python -m http.server)
sleep 3

# echo "::group::Testing vncserver with netcat (inside container)"
docker exec $container_id bash -c 'nc -v -w1 127.0.0.1 5901' 2>&1 | tee output-inside.txt
cat output-inside.txt  | grep --quiet RFB && echo "Passed inside test"  || { echo "Failed inside test" && TEST_OK=false; }
# echo "::endgroup::"

# echo "::group::Testing vncserver with netcat (outside container)"
nc -v -w1 127.0.0.1 5901 2>&1 | tee output-outside.txt
cat output-outside.txt | grep --quiet RFB && echo "Passed outside test" || { echo "Failed outside test" && TEST_OK=false; }
# echo "::endgroup::"

# echo "::group::Testing vncserver with netcat (inside container)"
docker exec $container_id bash -c 'nc -v -w1 127.0.0.1 5901' 2>&1 | tee output-inside.txt
cat output-inside.txt  | grep --quiet RFB && echo "Passed inside test"  || { echo "Failed inside test" && TEST_OK=false; }
# echo "::endgroup::"

# echo "::group::vncserver logs"
# docker exec $container_id bash -c "cat ~/.vnc/*.log"
# echo "::endgroup::"

docker stop $container_id > /dev/null
# if [ "$TEST_OK" == "false" ]; then
#     echo "One or more tests failed!"
#     exit 1
# fi