## AWS set up

### Set up an EC2 instance  

Location: Frankfurt.

Choose AMI (Amazon Machine Image). Select Ubuntu 22.04

Choose General purpose t2.micro (Free Tier Eligible)

Storage: free tier eligible up to 30 GB.

Security Group: SG-Webservers

VPC: Lab_VPC - 10.0.10.0/24 - Frankfurt (eu-central-1)

Correct subnet: Private-ec1a

Review and launch instance

Create a key pair and store it somewhere you will remember (You don’t really need a key pair, but can create a private key pair - for example if you need to log in via a SSH client on port 22)

Launch instance

Wait until Instance State change to “running” and status check is done before going to the next step

 

### Connect EC2 to Load Balancer

You need to register the instance to the right “Target Group” under “Load Balancing”

Correct target group is “Shiny-servers”



### NAT gateway

Does not need to do anything here

Route table on private subnet - entry for NAT gateway 

Destination: 0.0.0.0/0

Target: NAT gateway



### Connect to server using AWS Console in browser - “Connect” in AWS EC2

Connects via SSH but without the need for key pair

Go to EC2 Dashboard then Connect

Select: “Connect using EC2 Instance Connect Endpoint”

Select Endpoing: “EC2-Connect-Endpoint”

 

We use certificates provided by AWS (ACM - AWS Certificate Manager) placed on the Load Balancer


## Setup of Ubuntu 22.04

Refer to this tutorial:

https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04 

First thing: sudo apt update (Updates all Ubuntu modules)

In the tutorial you only need to do Step 4 and can ignore the rest.



Use the file editor nano that is built-into Ubuntu for making minor changes to app files and config-files.

 

Also:

Check that Python is available

Command: `sudo python3 --version`


## Setup on NgInx

Follow this tutorial in every detail:

https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04 

EXCEPT:

Do NOT choose `sudo ufw allow 'Nginx HTTP'` in step 2

Choose `sudo ufw allow 'Nginx Full'`

The setup is identical for Nginx on Ubuntu 22.04 and 20.04



## Setup shiny server

Setup virtual enviroment

Before you install Shiny server you should set up a virtual environment on the Ubuntu instance

As described in this tutorial section 2.1:

https://blog.zarathu.com/posts/2022-08-26-shinyforpython/ 



We first also need to install the python3.10-venv package to create virtual enviroments'



Create virtual environment: `python3 -m venv venv` (while you are in the myapp-folder)

Activate the virtual environment: `source venv/bin/activate`

Then `pip install shiny`



NB: All python packages (including the shiny package) should be installed in the virtual environment

The app code needs to be placed inside the myapp folder in venv



Then follow these tutorials:
- https://shiny.posit.co/py/docs/deploy.html#install
- https://www.digitalocean.com/community/tutorials/how-to-set-up-shiny-server-on-ubuntu-20-04

 



The virtual environment venv can be deployed at root, but must be copied over to `/srv/shiny-server/` for Shiny server is to find the app



Again: Don’t install a Python package necessary for the app directly at root. As it could interfere with OS (it uses Python)

Make sure to install latest version of Shiny Server as earlier ones do not work with Python

Version of Shiny server for Python installed for innlab.dzr.mk : 1.5.20.1002



### Special note:

In step 3 of the Digital Ocean tutorial you have the code below. As we run the innlab webapp in a private vpc the proxy_pass and proxy_redirect  needs to point to local IP, not public IP.

We made a new config file called `innlab.dzr.mk` as repelacement for the `example.com` file in the tutorial.
This code is thus included in the file `/etc/nginx/sites-available/innlab.dzr.mk`, and a shortcut for this file is added in this folder to the folder `/etc/nginx/sites-enabled`
As explained in https://www.charlesbordet.com/en/guide-shiny-aws/#3-set-up-a-reverse-proxy-with-nginx


```
location / {
       proxy_pass http://your_server_ip:3838;
       proxy_redirect http://your_server_ip:3838/ https://$host/;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection $connection_upgrade;
       proxy_read_timeout 20d;
   }
```



Transferring files from AWS S3 data bucket to the EC2 instance

Transfer is done by using the AWS CLI tools (must be installed): 

 

Command: `aws s3 cp s3-file-address ec2-destination-folder`
Transferring files directly to a EC2 system folder can be tricky, so it is recommended to first transfer the file to the instance home directory, and then move the file to the right directory using the bash `mv`command.

For example to transfer the app code from S3 to shiny server instance at `/srv/shiny-server/`



### Special note 2:

It is a known problem that installing packages in the virtual environment while on shiny server can be problematic. 

It is therefore recommended to install all packages while in the virtual envonment under myapp. 

When all desired packages are installed copy the virtual environment to the shiny server.



### Trouble shooting Shiny server:

Check log-files for shiny server, found at `/var/log/shiny-server`

use `sudo tail logfile-name.log` to check for the latest error messages

Se part 4 of:
https://www.charlesbordet.com/en/guide-shiny-aws/#4-how-to-debug-a-shiny-app-with-the-logs 



### Domain name

Uses SAO subdomain: innlab.dzr.mk via AWS Route 53



### References

1. Setting up EC2 instance: 

https://medium.com/nerd-for-tech/how-to-create-a-ubuntu-20-04-server-on-aws-ec2-elastic-cloud-computing-5b423b5bf635 

2. Installing modules on ubuntu: 

https://askubuntu.com/questions/95037/what-is-the-best-way-to-install-python-packages 

3. ShinyPython: 

https://blog.zarathu.com/posts/2022-08-26-shinyforpython/ 

 4. The ultimate guide for Shiny server on AWS:

https://www.charlesbordet.com/en/guide-shiny-aws/#
