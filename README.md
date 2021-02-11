# Recommendation Engines
A collection of Recommendation Engines and a simple API for deployment
Feb 2021

## Usage

Run the API with uvicorn:
```
$ uvicorn src.app:app --reload --host 0.0.0.0 --port 5000
```

or experiemnt with the induvidual models in /tests.

## Install

```
pip3 install requirments.txt
```

## Experimentation

There are test files in ```/tests``` which are simple examples of how to preprocess and pass data into the models, as well as a sample dataset.