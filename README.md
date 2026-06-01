\# xG Predictor — FIFA World Cup



A machine learning model that predicts Expected Goals (xG) 

for football shots using StatsBomb open data.



\## What is xG?

Expected Goals (xG) measures the probability of a shot 

resulting in a goal based on historical data. A shot with 

xG = 0.35 means historically 35% of similar shots result in a goal.



\## Data

\- FIFA World Cup 2018 and 2022

\- 3200 shots from 128 matches

\- Source: StatsBomb open data (free)



\## Model

\- XGBoost Classifier

\- AUC Score: 0.771

\- Features: distance, angle, body part, shot type, 

&#x20; technique, goalkeeper position, defenders in path



\## Project Structure

\- src/data.py — loads shot data from StatsBomb

\- src/features.py — calculates distance, angle, goalkeeper position

\- src/clean.py — cleans and prepares data

\- src/model.py — trains XGBoost model

\- src/predict.py — makes predictions

\- src/api.py — FastAPI REST endpoint

\- frontend/index.html — web interface



\## How to Run

pip install -r requirements.txt

python src/data.py

python src/clean.py

python src/model.py

uvicorn src.api:app --reload



\## API Usage

http://127.0.0.1:8000/predict?distance=15\&angle=40\&body\_part=right\&shot\_type=openplay\&technique=normal



\## Known Limitations

\- Free kick xG may be slightly high without tracking data

\- Defender positions are approximate

\- Model trained on World Cup data only

