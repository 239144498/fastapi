#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：iptv-web-sniff 
@File    ：a1.py
@IDE     ：PyCharm 
@Author  ：Naihe
@Date    ：2022/7/15 16:02 
"""
import json
import os
import uvicorn
import random
import requests
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from typing import Optional
from fastapi import FastAPI
from base64 import b64encode, b64decode

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World from FastAPI"}


@app.get("/hello/")
def aa():
    return {"data": "你好"}


@app.get("/list/")
def bb():
    return []


@app.get("/dict/")
def ssss():
    return {}


@app.post("/decrypt/")
def decrypt(info:str):
    key = bytes(os.getenv("key").encode())
    iv = bytes(os.getenv("iv").encode())
    ciphertext = b64decode(info)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    info = json.loads(plaintext.decode('utf-8'))
    return info


@app.post("/pull/")
def pull(fn:str=os.getenv("fn"), fs:str=os.getenv("fs")):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    raw = os.getenv("raw")%(fn, fs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = bytes(json.dumps(raw), 'utf-8')
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    value = b64encode(ciphertext).decode('utf-8')
    
    url = os.getenv("url")
    data = {'value': value}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'
    info = json.loads(response.text)
    return info    


# get random number between min(default:0) and max(default:9)
@app.get("/random/")
def get_random(min: Optional[int] = 0, max: Optional[int] = 9):
    rval = random.randint(min, max)
    return {"value": rval}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=5000)), log_level="info")
