#!/usr/bin/env bash
ansible-playbook devenv-playbook.yml
docker rm -f bitbucket
docker run --name bitbucket -e CONTEXT_PATH=ROOT -p 7990:7990 -p 7999:7999 -d bitbucket
v/bin/python scripts/forms.py