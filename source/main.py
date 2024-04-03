from fastapi import FastAPI
from fastapi.responses import JSONResponse
from client_telem import client_telem


source_client = client_telem()
app = FastAPI()

@app.get('/SOURCE/{ch}')
async def source(ch: int, current: float, voltage: float):
    comm = (ch, current, voltage)
    source_client.turn_on((comm))
    print(f'SOURCE {comm}')
    return JSONResponse({'SOURCE': ch, 'CURRENT': current, 'VOLTAGE': voltage})

@app.get('/OUTPUT/{ch}')
async def source(ch: int):
    source_client.turn_off(ch)
    return JSONResponse({'SOURCE': ch})


@app.get('/MEASURE')
async def source():
    telem = source_client.telem
    return telem