from fastapi import FastAPI
from pydantic import BaseModel
from source.client_telem import *


class MyFastAPI(FastAPI):#modify fastapi
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.communicator = client_telem()