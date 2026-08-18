<div align="center">

<img width=200 src="https://github.com/vikwritescode/derivative-frontend/blob/main/public/derivative.svg">

# Derivative: An Open Source BP Debate Tracker

</div>

Currently live on [derivative.lol](https://derivative.lol). This is the back-end of a tracker designed for British Parliamentary debating, allowing users record and import results, view their history, and access summary statistics. The front-end is visible [here](https://github.com/vikwritescode/bp-tracker-frontend)

Built with Python, FastAPI, Pydantic, pandas, Uvicorn, scikit-learn, and Firebase. All code is made available under the [GNU AGPLv3](https://github.com/vikwritescode/bp-tracker-frontend/blob/main/LICENSE.md) license.

## Features
- Add debate results
- Import from [TabbyCat](https://tabbycat.readthedocs.io/en/stable/) URLs
- Track performance over time
- View and manage history
- User registration and authentication
- Automatic motion categorisation

## Planned
- Improved motion categorisation model

## Setup Instructions

These are new setup instructions using docker. This guide will assume you already have docker and docker-compose set up to work on your machine. Instructions can be found [here](https://docs.docker.com), or you could ask a modern LLM, which should very much be able to guide you through the process.

This guide assumes you are using linux (or WSL).

### Firebase Configuration

You will need firebase credentials as this project uses firebase for authentication.
1. head to Firebase console
1. create a new project, enable Authentication
1. under project settings, go to the service accounts tab
1. generate a new private key and rename it to `serviceAccountKey.json`. **Do not share this with anyone.**
1. place this file in a folder 
    ```bash
    mkdir /some/folder/i/remember/my-dv-secrets
    cp downloaded/path/to/serviceAccountKey.json some/folder/i/remember/my-dv-secrets/serviceAccountKey.json
    ```
Remember this folder's path, as you will need it in the future.

### Motions JSON

This repository does not contain a list of motions to train the classifier model. I will not be providing instructions for getting a list of motions. However, I will assume you have a list of motions and topics in this format in your JSON:
```json
{
    "Motion": "This house supports capital controls restricting foreign currency during times of economic crises",
    "Infoslide": "Capital controls are government policies that regulate the flow money across a country's border",
    "Round": "Round 4",
    "Types": [
      "Economics",
      "International Relations"
    ]
}
```
Remember the path to this JSON, as it will come in useful.

### Docker Compose path setup 

1. Clone and enter the repository:
```bash
git clone https://github.com/vikwritescode/derivative
cd derivative
```
1. Ensure that all of these directories/paths are ready
    - path to your motions (in json form)
    - path to your secrets folder
    - path to an (empty) artifacts folder where your model will live

1. Find the blocks labelled `volume` and edit these lines accordingly wherever they exist:
    - `- ${HOME}/dv-secrets:/run/secrets:ro,Z` --> `- your/secrets/folder:/run/secrets:ro,Z`
    - `- ${HOME}/dv-artifacts:/artifacts:Z` --> `- your/artifacts/folder:/artifacts:Z`
    - `${HOME}/bp-debate-tracker/scraped_motions.json:/data/scraped_motions.json:ro,Z` --> `/your/path/to/motions.json:/data/scraped_motions.json:ro,Z`

### Training the model
1. Run the training command using docker-compose:
```bash
docker compose run --rm trainer
```
This should generate three files in in your artifacts folder: `classifier.pkl`, `multilabel_binarizer.pkl`, and `transformer.pkl`

### Running the service
1. Run the server
```bash
docker compose up -d --remove-orphans
```

At this stage, the server should be up and running at localhost:8000
