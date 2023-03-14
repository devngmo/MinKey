import os, sys
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_DIR)
sys.path.append(os.path.dirname(APP_DIR))

from shared import utils, global_variables
import apidefs

ALLOW_CREDENTIALS = utils.getEnvBool('ALLOW_CREDENTIALS', False)
ALLOW_ORIGINS = utils.getEnvValue('ALLOW_ORIGINS', '*').split(',')
ALLOW_METHODS = utils.getEnvValue('ALLOW_METHODS', '*').split(',')
ALLOW_HEADERS = utils.getEnvValue('ALLOW_HEADERS', '*').split(',')

utils.hl('------------------------------------')
utils.hl(f'  MinKey.API ver. {global_variables.version_name}')
utils.hl(f'  Build date {global_variables.build_date} Build number: {global_variables.build_number}')
utils.hl('------------------------------------')

app = FastAPI(openapi_tags=apidefs.tags_metadata, title='MinKey', version=global_variables.version_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ALLOW_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods = ALLOW_METHODS,
    allow_headers = ALLOW_HEADERS
)

from store import KeyStore
keyStore = KeyStore()
keyStore.load(os.getcwd())

@app.get("/")
def welcome():
    content = [
    '======= API ===========',
    'Add Value: /string/{key}  with plain/text body',
    'Get Value: /string/{key}',
    '======= Content ===========',
    ]
    dataMap = keyStore.getAll()
    for key in dataMap.keys():
        content += [f"{key}={dataMap[key]}"]
    return content

@app.delete("/keys")
def deleteAll():
    return keyStore.deleteAll()

@app.get("/string/{key}")
def getString(key:str):
    value = keyStore.getString(key)
    return PlainTextResponse(value)

@app.post("/string/{key}")
def setString(key:str, value:str=Body(media_type='plain/text')):
    return keyStore.setString(key, value)


