# Recommendation Engines
A collection of Recommendation Engines and a simple API for deployment

Feb 2021

Written in Python using ```FastAPI```, ```Numpy```, ```Tensorflow```.

## Usage

#### With Docker...
```
$ export DOCKER_BUILDKIT=0
$ docker image build -t reccomendation-engine-app .
$ docker run -p 5000:5000 --name re-app -d reccomendation-engine-app
```

The app will be live on http://localhost:5000

#### ...or without Docker
Run the API with uvicorn:
```
$ uvicorn src.app:app --reload --host 0.0.0.0 --port 5000
```

#### /Admin

The /admin page has a number of useful functions to interact with the API and view the stored data and predictions.

## API End Points

### Add Transaction Data
Pass in transactions to the ```/add``` endpoint to add these to the database. This will automatically populate user and item data tables.

**Request:**
- **user**: unique user id, [str]
- **item**: unique item id, [str]
- **rating**: The user assigned ordinal rating, [int]. Cannot be zero.

**Response:**
- **status**: 'success' if no errors, else 'error' as well as error infomation

```
curl --location --request POST 'http://0.0.0.0:5000/add' \
 --header 'Content-Type: application/json' \
 --data-raw '[{"user": "1", "item": "1", "rating": 1}, {"user": "2", "item": "4", "rating": 5}]'
```
### Fit the model
Call the ```/train``` endpoint to fit the model, passing in hyperparameters

**Request:**
- **epochs**: number of iterations, [int]. Default = 1000

**Response:**
- **status**: 'success' if no errors, else 'error' as well as error infomation

```
curl --location --request POST 'http://0.0.0.0:5000/train' \
--header 'Content-Type: application/json' \
--data-raw '{"epochs":700}'UserrecommendationRequest
```

### Get recomendations
Call the ```/reccomend-user``` endpoint to get item reccomendations for a user

**Request:**
- **user**: The user ID, [str]
- **count**: Number of reccomendations to return, [int]. Default = 100

**Response:**
- **user**: The user ID, [str]
- **recommendations**: A dictionary of recomendations in the format ```{"item id":predicted_rating}```

```
curl --location --request POST 'http://0.0.0.0:5000/train' \
--header 'Content-Type: application/json' \
--data-raw '{"epochs":700}'
```

or experiement with the induvidual models in ```tests```.

## Install

If not using docker, install the required packages:
```
pip3 install requirements.txt
```

## Experimentation

There are test files in ```tests``` which are simple examples of how to preprocess and pass data into the models, as well as a sample dataset.