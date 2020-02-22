import os
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import config
from reco import Reco

app = FastAPI()


class Items(BaseModel):
    ids: List[str]


class ItemsOutput(BaseModel):
    recommended_products: List[str] = []


@app.get('/ready',
         summary='Dummy URL for healthchecks',
         response_description='OK with status 200',
         )
def healthcheck():
    return 'OK', 200

@app.post('/recommend',
          response_model=ItemsOutput,
          summary='Items most relevant to given user',
          response_description='Recommended items',
          )
def recommend(user_items: Items):
    """
    - **user_items**: IDs of user items
    """
    recommended = app.reco.recommend(user_items.ids)
    return {'recommended_products': recommended}


if __name__ == '__main__':
    app.reco = Reco(f'{config.WORK_DIR}{config.MODEL_FILE}')
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
