# run.sh
#!/bin/bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
docker run -d -p 80:80 $DOCKERHUB_USERNAME/fastapi-todo