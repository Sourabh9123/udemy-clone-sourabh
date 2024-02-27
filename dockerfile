FROM python:3.12.0

WORKDIR /




# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# Copy the project code into the container at /code
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Expose port 8000 to the outside world
EXPOSE 8000



# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




# docker build -t my-image-app .   # this command will build image
# docker run -p 8000:8000 --name my-container-name my-image-app   # this command will image in container mensatation  first port is for localhost when you send api request and 
# secound port is for where your application is running like in django host setting for defaut it is 8000




# show all container --> docker ps
# stop container code --> docker stop id_or_name_of container for example --> docker stop c30004395e80
# delete container -- > docker rm   id_or_name_of container    --> docker rm abcdef123456
# image delete --> docker rmi  d_or_name_of container  --> docker rmi abcdef123456
# show all container including running and not running too  --> docker ps -a
# shows only running containers --> docker ps 
# docker start <container_name_or_id>   --> run existing container
# docker start -d <container_name_or_id> --> run existing container in background

# docker attach <container_name_or_id>  --> If you want to attach to the container's console (get access to its output), you can use docker attach:
# docker logs <container_name_or_id> --> If you want to see the logs of a running container without attaching to it, you can use docker logs:




# file directory    C:\Users\sourabh\Desktop\new_projects\udemy_clone\udemy_web_app_clone\dockerfile

#  docker push sourabhd081/my-new-image
# docker tag local-image:tagname username/repository:tagname    --> this is first step uploading process
# docker push username/repository:tagname  --> second step
# docker tag my-new-image sourabhd081/my-new-image 
# docker push sourabhd081/my-new-image
# docker container ls --> listing all container

# docker network ls --> listing network

# yml or yaml file bellow
# docker compose config
# docker compose up -d   --> if you remove -d it will occupie terminal 
# docker volume ls
# docker compose down  --> it removes all containers
# docker compose ps
# docker compose down --volumes
# docker compose -f docker-compose.dev.yml up -d --> this for if you want to run another docker compose file 
## docker compose -f docker-compose.dev.yml down --volumes
# docker compose exec db mysql -u root -p



##