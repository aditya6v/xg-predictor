# xG Predictor — Football Expected Goals

A machine learning model that predicts Expected Goals (xG) 
for football shots using StatsBomb open data.

## Live Demo
Frontend: https://aditya6v.github.io/xg-predictor
API: https://aditya-xg-predictor.onrender.com

## What is xG?
Expected Goals (xG) measures the probability of a shot 
resulting in a goal based on historical data. A shot with 
xG = 0.35 means historically 35% of similar shots result 
in a goal.

## Data
- FIFA World Cup 2018 and 2022
- La Liga 2016/17 to 2020/21 (Barcelona matches)
- Champions League 2015/16, 2017/18, 2018/19
- 7,452 shots total after cleaning
- Source: StatsBomb open data (free tier)

## Model
- XGBoost Classifier
- AUC Score: 0.810
- Penalties handled separately with fixed xG of 0.76
- Features:
  - Distance to goal
  - Shot angle (law of cosines)
  - Body part (head, left foot, right foot)
  - Shot type (open play, corner, free kick)
  - Technique (normal, volley, half volley, lob)
  - Goalkeeper distance to goal centre
  - Number of defenders in shot path
  - First time shot, open goal, under pressure flags

## Project Structure
- src/data.py — loads shot data from StatsBomb
- src/features.py — calculates distance, angle, goalkeeper position, defenders
- src/clean.py — cleans and prepares data
- src/mod
