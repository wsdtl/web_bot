# -*- coding: utf-8 -*-
import uvicorn
import socket
import ujson as json
from fastapi import FastAPI

from nonebot.log import logger

from help_data import __root_help__

app = FastAPI()

HOST: str = "127.0.0.1"
PORT: int = 20001

@app.get("/")
def root():
    return {"code":200, "msg" : __root_help__}

@app.get("/xiuxian/{txt}")
async def xiaonan(txt: str = ""):
    
    logger.success(f"收到 {txt}")

    if txt == "":
        return {"code": 200, "msg" :"404 err"}
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(HOST), PORT))
        
        data = {"msg": txt}
        json_data = json.dumps(data)
        s.send(bytes(json_data.encode('utf-8')))

        msg = json.loads(s.recv(1024))
        s.close()
        
    except Exception as e:
        
        logger.error(e)
        s.close()
        return {"code":200, "msg" :"404 err"}
    
    logger.success(f"{txt} 处理已完成")
    return {"code":200, "msg": msg}


if __name__ == '__main__':
    uvicorn.run('api:app', host="0.0.0.0", port=80, reload=False, access_log=True)
    
# uvicorn api:app --host '0.0.0.0' --port 8090 --reload
