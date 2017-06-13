# bitbucket-docker-automated

Docker Image and Python script to automagically start a Bitbucket instance inside Docker

# Requirements

* Docker
* Ansible
* Python 2.7
* Python Library: Requests

# How-To

0) Install the virtual environment
    * ansible-playbook devenv-playbook.yml
1) Build the docker image for bitbucket
    * docker build bitbucket/. -t bitbucket
2) Run the Docker Container
    * docker run --name bitbucket -e CONTEXT_PATH=ROOT -p 7990:7990 -p 7999:7999 bitbucket
3) Place your bamboo key next to the script file
    * file name should be "bitbucketkey"
    * Make sure it is in the proper format, there are some formatting issues with this file.  There should be slashes in the key itself
4) Run the script
    * v/bin/python scripts/forms.py
    * you should see a number of print lines while it is working, expect to see
        * Atlassian Bitbucket is starting up
    * Once everything has run, you should see: build complete


# Details

 * The docker container itself was lifted from "descoped/bitbucket".  Updating the line in the file to the latest version number should get you a later bitbucket, but I cannot guarantee the script will work
 * The virtual environment / playbook / Ansible / requirements text files are all optional.  You can just install requests directly to your python if you'd like, but I find this easier and more stable for reproduction
  