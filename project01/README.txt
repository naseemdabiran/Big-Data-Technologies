Naseem Dabiran
CIS 9760 - Big Data Technologies
Project01 


How to build docker and run the docker image:
---------------------------------------------

Docker is containerization software that allows for reproducibility of results and is portable to other machines. A docker image is an executable package that includes everything needed to run a container, including the code, runtime, libraries, configuration files, and environment variables. A Docker image is built by creating a Dockerfile that describes the application, dependencies and how to run it. A Dockerfile is a text image that creates docker images and containers by first initializing the base image and the commands it should execute.

The instructions included in Dockerfile for this project are (also available in project01 folder):

# We want to go from the base image of python:3.9
FROM python:3.9
# This is the equivalent of “cd /app” from our host machine
WORKDIR /app
# Let’s copy everything into /app
COPY .  /app
# Installs thedependencies. Passes in a text file.
RUN pip install -r requirements.txt
# This will run when we run our docker container
ENTRYPOINT ["python", "src/main.py"]

Within the terminal, we use docker build -t my_image:1.0 . to build the docker image called my_image:1.0. We then use docker run my_image:1.0 to build the image from the container and execute the program. Within the scope of the project, we must also include the environmental variables and command line arguments. In this case, the docker run command becomes: 
docker run \
-e DATASET_ID="8m42-w767" \
-e APP_TOKEN="YOUR_API_KEY"\ 
-e ES_HOST="YOUR_DOMAIN_ADDRESS" \
-e ES_USERNAME="YOUR_DOMAIN_USERNAME" \
-e ES_PASSWORD="YOUR_DOMAIN_PASSWORD" \
-e INDEX_NAME="fire" \
my_image:1.0 --page_size=1000 --num_pages=100

DATASET_ID, APP_TOKEN, ES_HOST, ES_USERNAME, ES_PASSWORD, and INDEX_NAME are environmental variables, while page_size and num_pages are command line arguments. If num_pages is not provided, the script will continue requesting data until all of the rows (except for those with null values for starfire_incident_id and incident_datetime) have been queried. 

APP_TOKEN is your API Key for NYC Open Data. ES_HOST is the OpenSearch Domain endpoint URL. ES_USERNAME is the OpenSearch Domain's username. ES_PASSWORD is the OpenSearch Domain's password. INDEX_NAME is the name of the index are creating in the OpenSearch Domain. 
 

Background information about the project:
-----------------------------------------

The goal of this project was to gather NYC fire incident dispatch data from NYC Open Data using AWS' services such as EC2, ElasticSearch and Kibana (OpenSearch). Utilizing EC2 and containerization via Docker, the data was loaded into an OpenSeach domain (ElasticSearch). Over 5 million records of fire incidents from 2004 to 2021 were downloaded, including the the ID, date and time, number of engines assigned, total response time, NYC borough, classification type, and if it was a valid response time for each incident. After the data was defined in the OpenSearch Dashboard (Kibana), analysis was performed on the data by creating unique visuals. 


Visuals-related questions and their answers:
---------------------------------------------

The visuals are available in the assets folder.

Does the higher number of engines assigned indicate a higher average incident response time? 
visual01 is a line graph that depicts the average incident response time in seconds on the y-axis and the number of engines assigned on the x-axis. There does not appear to be a correlation between average incident response time and number of engines assigned, and the average incident response time points appears to become less stable as the number of engines increases past 40 engines. The average response time does appear to be around 275 for less than 15 engines assigned. 

Which borough had the highest number of incidents? Which borough had the shortest average response time?
visual02(a) is a bar chart that depicts the count of incidents for each borough. Brooklyn had the highest number of incidents (over 1,600,000), followed by Manhattan, Queens, Bronx, and Staten Island (around 300,000). visual02(b) is a bar chart that depicts the average response time in seconds for each borough. Interestingly enough, Brooklyn had the lowest average response time of 244.49 seconds while Queens has the highest average response time of 283.23 seconds. This is interesting to note that the borough with the highest count of incidents had the lowest average response time.

Are the response times within an acceptable limit?
visual03 is a pie chart that depicts the proportion of valid response times, Y being Yes and N for No. The pie chart shows that a little less than 15% of response times were not within acceptable limits, which is 300 seconds according to the National Fire Protection Association (NFPA). The data shows that reforms are needed to improve response times and increase the percentage of valid response times.

What are the leading incidents classifications? 
visual04 is a horizontal bar chart that depicted the count of incidents for the top 10 incident classifications. The 3 out of the top 5 incident classifications is related to Medical Emergencies. This highlights the need for paramedics and EMS units. Other top incident classifications are related to Utility Emergencies for Water, Electric, and Gas.  
Unfortunately, Unwarranted Alarm Systems are also a part of the top ten incident classifications. This shows an avoidable waste of resources. 

Which incidents classifications have the highest average response time? 
visual05 is an area plot that depicted the top 5 incident classifications with the highest average response time, broken up by if they were considered valid response times or not. Elevator Emergency-Undefined had the highest average incident response time of about500 seconds, and all the times were valid. Elevator Emergency-Undefined had the lowest average incident response time of about 400 seconds for the valid response times, but about 600 seconds for the not valid response times. It is interesting to note the incident classification Medical-Serious Life Threatening had a incident response time of about 400 seconds for the valid response times, and about 600 seconds for the not valid response times, which is not ideal when a person's life is in danger. It is also concerning that is has one of the highest average incident response times. 



