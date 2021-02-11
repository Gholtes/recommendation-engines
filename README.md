# Recommendation Engines
A collection of Recommendation Engines and a simple API for deployment

Feb 2021

Written in Python using ```FastAPI```, ```Numpy```, ```Tensorflow```.

## Usage

Run the API with uvicorn:
```
$ uvicorn src.app:app --reload --host 0.0.0.0 --port 5000
```

#### Add Transaction Data
Pass in transactions to the ```\add``` endpoint to add these to the database. This will automatically populate user and item data tables.

**Arguments:**
- **user**: unique user id, [str]
- **item**: unique item id, [str]
- **rating**: The user assigned ordinal rating [int]. Cannot be zero.

**Returns:**
- **status**: Success of addition

```
curl --location --request POST 'http://0.0.0.0:5000/add' \
 --header 'Content-Type: application/json' \
 --data-raw '[{"user": "1", "item": "1", "rating": 1}, {"user": "2", "item": "4", "rating": 5}]'
```
#### Fit the model
Call the ```/train``` endpoint to fit the model, passing in hyperparameters

```
curl --location --request POST 'http://0.0.0.0:5000/train' \
--header 'Content-Type: application/json' \
--data-raw '{"epochs":700}'
```


or experiement with the induvidual models in /tests.

## Install

```
pip3 install requirments.txt
```

## Experimentation

There are test files in ```/tests``` which are simple examples of how to preprocess and pass data into the models, as well as a sample dataset.