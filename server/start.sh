#!/bin/bash

export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

sdk env

# kill all java processes
killall java
# java -jar target/scim-ai-server.jar > /dev/null 2>&1 &
java -jar target/scim-ai-server.jar &
GET_USER_RESULT=$(curl --connect-timeout 1 --max-time 1 -s --no-progress-meter -X GET http://localhost:8080/scim/v2/Users)
# wait until the server is up and running
echo "$GET_USER_RESULT"
MAX_ATTEMPTS=15
ATTEMPT=0
while [[ $GET_USER_RESULT != *"ListResponse"* && $ATTEMPT -lt $MAX_ATTEMPTS ]]; do
  echo "Waiting for the server to return list users response (Attempt: $((ATTEMPT+1)))"
  sleep 1
  GET_USER_RESULT=$(/usr/bin/curl --connect-timeout 1 --max-time 1 -s --no-progress-meter -X GET http://localhost:8080/scim/v2/Users)
  echo "$GET_USER_RESULT"
  ((ATTEMPT++))
done
killall java
exit 0;