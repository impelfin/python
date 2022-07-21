# python

### python base python:latest

### Container execute		    
docker run -d -it --name python -p 8000:8000 -v /Users/lune/Documents/GitHub/python:/app impelfin/python

### Container shell connection
docker exec -it python /bin/bash
