# 🥗 AI Personalized Diet Recommendation System

## Overview

An AI-powered diet recommendation system that generates personalized food recommendations, calorie targets, BMI analysis, nutrition insights, and 12-week meal plans based on user health metrics and fitness goals.

## Features

- BMI Analysis
- BMR Calculation
- TDEE Calculation
- Daily Water Intake Recommendation
- Daily Protein Requirement Calculation
- Personalized Food Recommendations
- 3-Month Meal Plan Generator
- Macronutrient Analysis
- AI Nutrition Assistant using Gemini API
- Downloadable Meal Plans

## Machine Learning

Model Used:
- Random Forest Classifier

Input Features:
- Gender
- Age
- Height
- Weight
- BMI
- Meals Per Day
- BMR
- Water Intake
- Protein Requirement

Output:
- Thin
- Medium
- Fit
- Advance Fit

## Datasets

### USDA FoodData Central
Used for:
- Calories
- Protein
- Carbohydrates
- Fat
- Fiber

### BMI Dataset
Used for:
- BMI Classification
- Health Status Analysis

### Calorie Dataset
Used for:
- Daily Calorie Requirement Estimation

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- Streamlit
- Joblib
- Google Gemini API

## Project Structure

```text
python/
├── app.py
├── gemini_chatbot.py
├── meal_plan_generator.py

Cleaned_data/
├── cleaned_nutrition_dataset.csv
├── cleaned_bmi_dataset.csv
├── cleaned_calorie_dataset.csv

models/
└── diet_recommendation_model.pkl
```

## Installation

```bash
git clone <repository-url>
cd AI-Personalized-Diet-Recommendation-System

pip install -r requirements.txt
```

## Run Application

```bash
streamlit run python/app.py
```

## Future Improvements

- Ranking-based food recommendation engine
- Goal-specific meal plans
- Weekly progress tracking
- User authentication
- Cloud deployment

## Author

Vinod Vinu
