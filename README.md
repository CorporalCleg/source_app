##  - Setting up envirnoment

```
poetry install
```

##  - start server

```
poetry run python3 source/server.py
```

##  - start app. (in another terminal)

```
cd source && poetry uvicorn  main:app --reload
```




|     request  |req. example|
|-------|------------|
| make measurement    | /MEASURE                           |
| turn on channel # x | /SOURCE/2?current=3.0&voltage=4.0  |
| turn on channel # x | /OUTPUT/3                          |
