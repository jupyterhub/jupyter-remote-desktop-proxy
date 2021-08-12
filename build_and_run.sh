docker build -t $(whoami)/$(basename ${PWD}) .
docker run --rm  -p 8888:8888 $(whoami)/$(basename ${PWD})