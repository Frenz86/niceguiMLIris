# pip install scalar-fastapi
import frontend
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, ORJSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference
from pathlib import Path
import pandas as pd
import uvicorn
import joblib


class Features(BaseModel):
    feature1: float = 3.0
    feature2: float = 3.0
    feature3: float = 3.0
    feature4: float = 3.0
    # description: Optional[str] = None questo è un campo opzionale


classes = {
            0: 'setosa',
            1: 'versicolor',
            2: 'virginica',
            }

MODEL_PATH1 = Path('iris.pkl')
MODEL_PATH2 = Path('')  # to load different models
model = {}


@asynccontextmanager  # @app.on_event is deprecated
async def mlmodel(app: FastAPI):
    with open(MODEL_PATH1, 'rb') as file:
        model["iris_reg"] = joblib.load(file)
    # model["iris_reg2"] = joblib.load(MODEL_PATH2)
    yield
    model.clear()

app = FastAPI(lifespan=mlmodel,
              default_response_class=ORJSONResponse,
              title="API IRIS Dataset",
              description="with FastAPI by Daniele Grotti",
              version="1.0")


@app.get("/home", status_code=status.HTTP_200_OK)
def home():
    return {" ---->          http://localhost:8000/scalar     <----------"}

##############################################################################
# go to http://127.0.0.1:8000/scalar
# from scalar_fastapi import get_scalar_api_reference


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
                                    openapi_url=app.openapi_url,
                                    title=app.title + " - Scalar",
                                    )


# #################  GET  ##############################
@app.get("/predict", status_code=status.HTTP_200_OK)
async def predict_get(data: Features = Depends()):
    try:
        data_df = pd.DataFrame(data).T
        data = data_df.iloc[1:]
        y_pred = classes[model["iris_reg"].predict(data).tolist()[0]]

        # return {'prediction': y_pred}
        return StreamingResponse(iter([ORJSONResponse(y_pred).body]), media_type = "application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# #################  POST  ##############################
@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict_post(data: Features = Depends):
    try:
        data_df = pd.DataFrame(data).T
        data = data_df.iloc[1:]
        y_pred = classes[model["iris_reg"].predict(data).tolist()[0]]

        # return {'prediction': y_pred}
        return StreamingResponse(iter([ORJSONResponse(y_pred).body]), media_type = "application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# #################  PUT  #####################################################
@app.put("/predict", status_code=status.HTTP_200_OK)
async def predict_put(data: Features = Depends()):
    try:
        data_df = pd.DataFrame(data).T
        data = data_df.iloc[1:]
        y_pred = classes[model["iris_reg"].predict(data).tolist()[0]]

        # return {'prediction': y_pred}
        return StreamingResponse(iter([ORJSONResponse(y_pred).body]), media_type = "application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# #################  to visualize in a swagger images  ########################
@app.get("/image", status_code=status.HTTP_200_OK)
async def get_image(animal: str):
    try:
        file_path = Path(f'img/{animal}.jpg')
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        file = open(file_path, mode="rb")
        return StreamingResponse(file, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


###############################################################################
###############################################################################
frontend.init(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
