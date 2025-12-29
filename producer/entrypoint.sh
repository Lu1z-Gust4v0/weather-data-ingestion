#!/bin/bash

# Export environment variables so Cron can see them
# Cron jobs run in a clean shell, so they miss Docker ENV variables otherwise
printenv | grep -v "no_proxy" >> /etc/environment

# Start the cron daemon in the foreground
echo "Cron service starting..."
cron -f