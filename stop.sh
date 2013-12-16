#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | awk '{ print $2 }' | xargs kill