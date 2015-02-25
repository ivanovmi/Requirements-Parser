#!/bin/bash

echo "$2" | mail -s "Merged requires from $(date "+%Y-%m-%d %H:%M")" "$1"