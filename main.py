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


@app.get("/decrypt/")
def aax(info:str):
    key = os.getenv("key")
    iv = os.getenv("iv")
    ciphertext = b64decode(info)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    info = json.loads(plaintext.decode('utf-8'))
    return info


# get random number between min(default:0) and max(default:9)
@app.get("/random/")
def get_random(min: Optional[int] = 0, max: Optional[int] = 9):
    rval = random.randint(min, max)
    return {"value": rval}


if __name__ == "__main__":
    uvicorn.run("a1:app", host="0.0.0.0", port=int(os.getenv("PORT", default=5000)), log_level="info")
