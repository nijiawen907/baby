import os
import threading

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

import globals
from exception import register_exception
from predict.detect import Predictor
from sql import get_last_scene, get_happy_scenes

app = fastapi.FastAPI()

predictor = Predictor()

register_exception(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get('/get_res')
async def get_res():
    print(globals.get_pose_status())
    print(globals.get_expression_status())
    last_result = get_last_scene()
    if not globals.get_pose_status() and not globals.get_expression_status():

        return {"code": 1, "data": None}

    # elif last_result[2] == 'Happy':
    #     return {"code": 1, "data": None}

    elif globals.get_pose_status():
        res_data = {
            "id": last_result[0],
            "image_path": last_result[1],
            "status": last_result[2],
            "text": "危险动作",
            "created_time": last_result[3],
        }
        return {"code": 1, "data": res_data}

    elif globals.get_expression_status():
        res_data = {
            "id": last_result[0],
            "image_path": last_result[1],
            "status": last_result[2],
            "text": "哭闹",
            "created_time": last_result[3],
        }
        return {"code": 1, "data": res_data}


@app.get('/happy_scene')
async def get_happy_scene():
    results = get_happy_scenes()
    return_data = []
    for res in results:
        res_data = {
            "id": res[0],
            "image_path": res[1],
            "status": res[2],
            "created_time": res[3],
        }
        return_data.append(res_data)
    return {"code": 1, "data": return_data}


@app.get("/image/{image_name:path}")
async def get_image(image_name: str):
    # 读取图像文件
    image_path = f'{image_name}'
    # image_path = image_name.replace('+', '/')
    return FileResponse(image_path, media_type="image/jpeg")


@app.get("/")
async def root():
    print(globals.expression_status)
    return {"message": globals.expression_status}


if __name__ == '__main__':
    # 创建并启动推理线程
    thread = threading.Thread(target=predictor.predict_video, daemon=True)
    thread.start()

    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8001)
