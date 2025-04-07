import os, sys, json, yaml
from fastapi import FastAPI, Body, HTTPException, Header
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
AUTO_SAVE = utils.getEnvBool('AUTO_SAVE', True)
TRACE_ENABLED = utils.getEnvBool('TRACE_ENABLED', False)
DATA_FOLDER = utils.getEnvValue('DATA_FOLDER', None)
if DATA_FOLDER == None:
    DATA_FOLDER = os.path.join(os.path.dirname(APP_DIR), 'data')
    
utils.hl('------------------------------------')
utils.hl(f'  MinKey.API ver. {global_variables.version_name}')
utils.hl(f'  Build date {global_variables.build_date} Build number: {global_variables.build_number}')
utils.hl(f'  Storage Folder: {DATA_FOLDER}')
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
keyStore = KeyStore(autoSave=AUTO_SAVE, traceEnabled=TRACE_ENABLED)
keyStore.load(DATA_FOLDER)

from list_mgr import ListManager
listMgr = ListManager()
listMgr.load()

@app.get("/")
def welcome():
    content = [
    '======= API ===========',
    'Add Value: /string/{key}  with plain/text body',
    'Get Value: /string/{key}',
    '======= Content ===========',
    ]
    for key in keyStore.store.keys():
        m = keyStore.store[key]
        content += [f"{key}: {len(m)} items"]
    return content

@app.delete("/keys")
def deleteAll():
    return keyStore.deleteAll()

@app.get("/string")
def getString(key:str = Header()):
    value = keyStore.getString(key)
    return PlainTextResponse(value)

@app.post("/string")
def setString(key:str = Header(), value:str=Body(media_type='plain/text')):
    return keyStore.setString(key, value)

@app.get("/json")
def getJson(key:str = Header()):
    if TRACE_ENABLED:
        print(f"[GET JSON] {key}...")
    value = keyStore.getString(key)
    if TRACE_ENABLED:
        print(value)
    if value == None:
        raise HTTPException(status_code=404, detail=f'Key not found: {key}')
    return json.loads(value)

@app.post("/json")
def setJson(key:str = Header(), value:dict=Body()):
    if TRACE_ENABLED:
        print(f"[SET JSON] {key}...")
    return keyStore.setString(key, json.dumps(value))

@app.get("/list/{listId}/{index}")
def list_get_item(listId:str, index: int):
    item = listMgr.getAt(listId, index)
    if item == None:
        raise HTTPException(status_code=404, detail='List is empty')
    return item


@app.post("/list/string/{listId}")
def list_append_string_item(listId:str, content: str = Body(media_type='text/plain')) -> str:
    print(f'LIST [{listId}] append')
    print(content)
    listMgr.append(listId, content)
    return PlainTextResponse('ok')

@app.post("/list/dict/{listId}")
def list_append_dict_item(listId:str, content: dict = Body()) -> str:
    print(f'LIST [{listId}] append')
    print(content)
    listMgr.append(listId, content)
    return PlainTextResponse('ok')

@app.delete('/list/{listId}/{index}')
def list_remove_item_at(listId: str, index: int):
    print(f"LIST [{listId}] remove at {index}...")
    listMgr.removeAt(listId, index)
