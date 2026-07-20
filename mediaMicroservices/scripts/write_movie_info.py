#!/usr/bin/env python

import aiohttp
import asyncio
import sys
import json
import argparse

async def upload_cast_info(session, addr, cast):
    path = addr + "/wrk2-api/cast-info/write"
    async with session.post(path, json=cast) as resp:
        body = await resp.text()
        if resp.status != 200:
            print("\n\n===========================")
            print(path, cast)
            print(resp.status, body)
            print("===========================")
        return body

async def upload_plot(session, addr, plot):
    path = addr + "/wrk2-api/plot/write"
    async with session.post(path, json=plot) as resp:
        body = await resp.text()
        if resp.status != 200:
            print("\n\n===========================")
            print(path, plot)
            print(resp.status, body)
            print("===========================")
        return body

async def upload_movie_info(session, addr, movie):
    path = addr + "/wrk2-api/movie-info/write"
    async with session.post(path, json=movie) as resp:
        body = await resp.text()
        if resp.status != 200:
            print("\n\n===========================")
            print(path, movie)
            print(resp.status, body)
            print("===========================")
        return body

async def register_user(session, addr, user):
    params = {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "password": user["password"]
    }
    path = f"{addr}/wrk2-api/user/register"
    async with session.post(path, data=params) as resp:
        body = await resp.text()
        if resp.status != 200:
            print("\n\n===========================")
            print(path, params)
            print(resp.status, body)
            print("===========================")
        return body

async def register_movie(session, addr, movie):
    params = {
        "title": movie["title"],
        "movie_id": movie["movie_id"]
    }
    path = addr + "/wrk2-api/movie/register"
    async with session.post(path, data=params) as resp:
        body = await resp.text()
        if resp.status != 200:
            print("\n\n===========================")
            print(path, params)
            print(resp.status, body)
            print("===========================")
        return body

async def write_cast_info(addr, raw_casts):
  idx = 0
  tasks = []
  conn = aiohttp.TCPConnector(limit=200)
  async with aiohttp.ClientSession(connector=conn) as session:
    for raw_cast in raw_casts:
      try:
        cast = dict()
        cast["cast_info_id"] = raw_cast["id"]
        cast["name"] = raw_cast["name"]
        cast["gender"] = True if raw_cast["gender"] == 2 else False
        cast["intro"] = raw_cast["biography"]
        task = asyncio.ensure_future(upload_cast_info(session, addr, cast))
        tasks.append(task)
        idx += 1
      except:
        print("Warning: cast info missing!")
      if idx % 200 == 0:
        resps = await asyncio.gather(*tasks)
        print(idx, "casts finished")
    resps = await asyncio.gather(*tasks)
    print(idx, "casts finished")

async def write_movie_info(addr, raw_movies):
  idx = 0
  tasks = []
  conn = aiohttp.TCPConnector(limit=200)
  async with aiohttp.ClientSession(connector=conn) as session:
    for raw_movie in raw_movies:
      movie = dict()
      casts = list()
      movie["movie_id"] = str(raw_movie["id"])
      movie["title"] = raw_movie["title"]
      movie["plot_id"] = raw_movie["id"]
      for raw_cast in raw_movie["cast"]:
        try:
          cast = dict()
          cast["cast_id"] = raw_cast["cast_id"]
          cast["character"] = raw_cast["character"]
          cast["cast_info_id"] = raw_cast["id"]
          casts.append(cast)
        except:
          print("Warning: cast info missing!")
      movie["casts"] = casts
      movie["thumbnail_ids"] = [raw_movie["poster_path"]]
      movie["photo_ids"] = []
      movie["video_ids"] = []
      movie["avg_rating"] = raw_movie["vote_average"]
      movie["num_rating"] = raw_movie["vote_count"]
      task = asyncio.ensure_future(upload_movie_info(session, addr, movie))
      tasks.append(task)
      plot = dict()
      plot["plot_id"] = raw_movie["id"]
      plot["plot"] = raw_movie["overview"]
      task = asyncio.ensure_future(upload_plot(session, addr, plot))
      tasks.append(task)
      task = asyncio.ensure_future(register_movie(session, addr, movie))
      tasks.append(task)
      idx += 1
      if idx % 200 == 0:
        resps = await asyncio.gather(*tasks)
        print(idx, "movies finished")
    resps = await asyncio.gather(*tasks)
    print(idx, "movies finished")

async def register_users(addr):
    conn = aiohttp.TCPConnector(limit=200)
    tasks = []
    async with aiohttp.ClientSession(connector=conn) as session:
        for idx in range(1, 1001):
            user = {
                "first_name": f"first_name_{idx}",
                "last_name": f"last_name_{idx}",
                "username": f"username_{idx}",
                "password": f"password_{idx}",
            }
            tasks.append(asyncio.ensure_future(register_user(session, addr, user)))
            if idx % 200 == 0:
                resps = await asyncio.gather(*tasks)
                print(idx, "users finished")
                tasks = []

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--cast", action="store", dest="cast_filename",
    type=str, default="../datasets/tmdb/casts.json")
  parser.add_argument("-m", "--movie", action="store", dest="movie_filename",
    type=str, default="../datasets/tmdb/movies.json")
  parser.add_argument("--server_address", action="store", dest="server_addr",
    type=str, default="http://127.0.0.1:8080")
  args = parser.parse_args()

  with open(args.cast_filename, 'r') as cast_file:
    raw_casts = json.load(cast_file)
  loop = asyncio.get_event_loop()

  future = asyncio.ensure_future(register_users(args.server_addr))
  loop.run_until_complete(future)

  future = asyncio.ensure_future(write_cast_info(args.server_addr, raw_casts))
  loop.run_until_complete(future)

  with open(args.movie_filename, 'r') as movie_file:
    raw_movies = json.load(movie_file)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(write_movie_info(args.server_addr, raw_movies))
    loop.run_until_complete(future)
