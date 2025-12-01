🔹 AWS Deployment Details

This Trivia Quiz application was deployed on an AWS EC2 instance running Ubuntu.

I used the following AWS services during deployment:
AWS EC2 – created a virtual server to host the website
Security Groups – configured inbound rules for HTTP (port 80)
SSH – connected to the instance and installed required packages
Docker – containerized the application and ran it on EC2
NGINX – used as a reverse proxy for serving the web app
Git – pulled the latest code directly from GitHub into the EC2 machine

Deployment Steps Summary:
Created an Ubuntu EC2 instance
Installed Docker and configured Docker service
Built a Docker image of the frontend
Ran the container on EC2
Exposed the application via port 80
