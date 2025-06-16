#!/usr/bin/env bash

for i in {1..10}; do
  username="username_"$i
  password="password_"$i
  title="title_"$i
  text=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 256 | head -n 1)
  curl -d "text="$text"&username="$username"&password="$password"&rating=5&title="$title \
      http://18.193.68.182:3009/wrk2-api/review/compose
done
 
