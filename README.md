## Setting up envirnoment

### - install requirements
```
pip3 install poetry
poetry install
```


## Start app
###  - start server

```
poetry run python3 source/server.py
```

###  - start app. (in another terminal)

```
poetry run python3 source/main.py
```




|     request  |req. example|
|-------|------------|
| make measurement    | /MEASURE                           |
| turn on channel # x | /SOURCE/2?current=3.0&voltage=4.0  |
| turn on channel # x | /OUTPUT/3                          |


## Tests

### - run tests
 
```
poetry run pytest tests/test_source.py
```