#!/bin/sh

ps auxw | grep cottage.py | grep -v grep > /dev/null

if [ $? != 0 ]
then
        systemctl restart thermoPICottage.service > /dev/null
fi

