#!/usr/bin/env bash

for i in {1..1000}; do
  echo "User $i"
  curl -d "first_name=first_name_"$i"&last_name=last_name_"$i"&username=username_"$i"&password=password_"$i \
      http://18.193.68.182:3009/wrk2-api/user/register
done
