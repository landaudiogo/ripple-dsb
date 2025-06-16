#!/usr/bin/env bash

for i in {1..1000}; do
  echo "Movie $i"
  curl -d "title=title_"$i"&movie_id=movie_id_"$i \
      http://18.193.68.182:3009/wrk2-api/movie/register
done
