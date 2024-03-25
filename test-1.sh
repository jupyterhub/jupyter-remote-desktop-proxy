# start a container with a tcp server spewing stuff on connect
container_id=$(docker run -d -v $(pwd):/mnt/test -p 5901:5901 --entrypoint python quay.io/consideratio/test:tiger /mnt/test/dummy-tcp-server.py)
sleep 1

# try connect to it from within the container
docker exec $container_id bash -c 'timeout --preserve-status 1 nc -v 127.0.0.1 5901' 2>&1 | tee output-inside.txt
cat output-inside.txt  | grep --quiet RFB && echo "Passed inside test"  || { echo "Failed inside test" && TEST_OK=false; }

# try connect to it from outside the container
timeout --preserve-status 1 nc -v 127.0.0.1 5901 2>&1 | tee output-outside.txt
cat output-outside.txt | grep --quiet RFB && echo "Passed outside test" || { echo "Failed outside test" && TEST_OK=false; }

# check logs from dummy tcp server
docker logs $container_id

# stop and do error code etc
docker stop -t0 $container_id > /dev/null
if [ "$TEST_OK" == "false" ]; then
    echo "One or more tests failed!"
    exit 1
fi
