#!/bin/bash
set -e

. docker-java-home

# allow the container to be started with `--user`
if [ "$1" = 'bin/start-bitbucket.sh' -a "$(id -u)" = '0' ]; then
    if [ ! -f $BITBUCKET_INST/conf/server.xml ]; then /configure; fi
    rm -f $BITBUCKET_HOME/.jira-home.lock
    chown -R $UID:$UID $BITBUCKET_INST
    chown -R $UID:$GID $BITBUCKET_HOME
    exec gosu $UID "$BASH_SOURCE" "$@"
fi

umask 0027
exec "$@"