from fastapi.responses import JSONResponse
from uvicorn import run
from source.my_app import MyFastAPI
import threading


app = MyFastAPI()

def logging():
    while True:
        app.communicator.collect_telem()

@app.get('/SOURCE/{channel}')
async def source(channel: int, current: float, voltage: float):
    comm = (channel, current, voltage)
    await app.communicator.turn_on((comm))
    print(f'SOURCE {comm}')
    return JSONResponse({'action': f"turn on channel # {channel}"})

@app.get('/OUTPUT/{channel}')
async def output(channel: int):
    await app.communicator.turn_off(channel)
    return JSONResponse({'action': f"turn off channel # {channel}"})


@app.get('/MEASURE')
async def source():
    telem = app.communicator.telem
    return telem

#logger thread
start_logging = lambda: threading.Thread(target=logging).start()


if __name__ == '__main__':
    start_logging()
    run(app, host="127.0.0.1", port=8000)
