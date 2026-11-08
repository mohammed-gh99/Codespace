# Codespace
deploy churn prediction model on docker
# Customer Churn Prediction API

A machine learning project that predicts whether a telecom customer is likely to churn. The trained scikit-learn model is exposed through a REST API built with FastAPI, validated with Pydantic, and packaged with Docker.

## Overview

This project takes customer information as JSON and returns:

- `churn_probability`: the model's estimated probability that the customer will churn.
- `churn`: a Boolean classification based on a threshold of `0.5`.

The prediction service uses a scikit-learn `Pipeline` containing a `DictVectorizer` and a `LogisticRegression` classifier. The fitted pipeline is saved to `model.bin` and loaded by the API when the application starts.

## How It Works

1. Customer data is sent to the `/predict` endpoint as JSON.
2. FastAPI uses the Pydantic `Customer` model to validate the request fields and values.
3. The validated customer object is converted to a dictionary.
4. The scikit-learn pipeline transforms the input and generates a churn probability.
5. The API returns the probability and the predicted churn label.

## Tech Stack

- **Python** — application and model code
- **pandas** — data handling
- **scikit-learn** — feature vectorization, model training, and prediction
- **FastAPI** — REST API
- **Pydantic** — request and response validation
- **Uvicorn** — ASGI server
- **uv** — Python dependency and environment management
- **Docker** — containerization

## Project Structure

```text
.
├── Dockerfile
├── model.bin
├── predict.py
├── train.py
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

`model.bin` contains the trained scikit-learn pipeline used by the prediction API.

## Run Locally

### 1. Requirements

- Python version compatible with the version specified in `.python-version` and `pyproject.toml`
- [uv](https://docs.astral.sh/uv/)

### 2. Install dependencies

From the project root, run:

```bash
uv sync
```

### 3. Start the API

```bash
uv run uvicorn predict:app --host 0.0.0.0 --port 9696 --reload
```

The API will be available at:

- API: `http://localhost:9696`
- Interactive API documentation: `http://localhost:9696/docs`

## API Usage

### Endpoint

```http
POST /predict
```

### Example request

```json
{
  "gender": "male",
  "seniorcitizen": 0,
  "partner": "no",
  "dependents": "yes",
  "phoneservice": "no",
  "multiplelines": "no_phone_service",
  "internetservice": "dsl",
  "onlinesecurity": "no",
  "onlinebackup": "yes",
  "deviceprotection": "no",
  "techsupport": "no",
  "streamingtv": "no",
  "streamingmovies": "no",
  "contract": "month-to-month",
  "paperlessbilling": "yes",
  "paymentmethod": "electronic_check",
  "tenure": 6,
  "monthlycharges": 29.85,
  "totalcharges": 129.85
}
```

### Example response

```json
{
  "churn_probability": 0.35,
  "churn": false
}
```

The response above is illustrative; the actual probability is calculated by the trained model. The `churn` label is `true` when the predicted probability is greater than or equal to `0.5`, and `false` otherwise.

## Run with Docker

Docker packages the API, its Python dependencies, and the saved model into a container.

### 1. Build the image

Run this command from the directory containing the `Dockerfile`:

```bash
docker build -t churn-prediction .
```

### 2. Start the container

```bash
docker run --rm -p 9696:9696 churn-prediction
```

Then open `http://localhost:9696/docs` to use the API documentation.

## Model Training

The training workflow is in `train.py`. To retrain the model and regenerate `model.bin`, run:

```bash
uv run python train.py
```

Make sure the training data required by `train.py` is available in the location expected by that script.

## Notes

- The API expects the customer fields and categorical values defined by the Pydantic `Customer` model in `predict.py`.
- The classification threshold is currently fixed at `0.5`.
- Keep the training and prediction preprocessing consistent: the saved pipeline is responsible for transforming incoming customer records before prediction.

