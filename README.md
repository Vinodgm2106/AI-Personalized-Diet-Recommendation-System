# 🥗 AI Personalized Diet Recommendation System

## 📌 Project Overview

The AI Personalized Diet Recommendation System is a Machine Learning and Nutrition Analytics application that provides personalized food recommendations, BMI analysis, calorie planning, macronutrient tracking, and a 3-month personalized meal plan based on user health metrics and fitness goals.

The project integrates USDA FoodData Central nutrition data, machine learning models, Streamlit, and Google Gemini API to deliver intelligent diet recommendations.

---

# 🏗️ Project Architecture

User Input
↓
BMI & Health Analysis
↓
Feature Engineering
↓
Machine Learning Model
↓
Food Recommendation Engine
↓
Meal Plan Generator
↓
Streamlit Dashboard
↓
AI Diet Assistant (Gemini API)

---

# 🚀 Features

### Health Analysis

- BMI Calculation
- BMI Classification
- BMR Calculation
- TDEE Estimation
- Water Intake Recommendation
- Daily Protein Requirement

### Personalized Food Recommendations

- Goal-based recommendations
- Nutrition-aware food filtering
- USDA FoodData Central integration

### Macronutrient Analysis

- Protein Tracking
- Carbohydrate Tracking
- Fat Tracking

### 3-Month Diet Planner

- 12-week meal plan
- Breakfast, Lunch, Dinner scheduling
- Daily calorie tracking
- Daily protein tracking
- CSV download support

### AI Diet Assistant

Powered by Google Gemini API.

Provides:

- Diet advice
- Weight loss guidance
- Muscle gain recommendations
- Workout suggestions
- Hydration recommendations

---

# 📊 Datasets Used

## USDA FoodData Central Dataset

Files Used:

- food.csv
- food_nutrient.csv
- nutrient.csv

Key Features:

- Food Name
- Calories
- Protein
- Carbohydrates
- Fat
- Fiber

Source:

https://fdc.nal.usda.gov/

---

## BMI Dataset

Features:

- Gender
- Age
- Height
- Weight
- BMI

Purpose:

BMI classification and fitness goal analysis.

---

## Calorie Dataset

Features:

- Gender
- Age
- Height
- Weight
- Activity Level
- Calories Required

Purpose:

Daily calorie estimation.

---

# ⚙️ Feature Engineering

## BMI

BMI = Weight / Height²

Purpose:

- Health assessment
- Fitness classification

## BMR

Male:

BMR = 10W + 6.25H − 5A + 5

Female:

BMR = 10W + 6.25H − 5A − 161

Purpose:

Calories burned at rest.

## TDEE

TDEE = BMR × Activity Factor

Purpose:

Daily calorie requirement.

## Water Intake

Water Intake = Weight × 0.033

Purpose:

Daily hydration recommendation.

## Protein Requirement

Protein Requirement = Weight × 1.6

Purpose:

Muscle maintenance and recovery.

---

# 🤖 Machine Learning Model

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

Target:

- Thin
- Medium
- Fit
- Advance Fit

Output:

Personalized fitness goal recommendation.

---

# 🖥️ Streamlit Dashboard

### User Inputs

- Gender
- Age
- Height
- Weight
- Meals Per Day
- Activity Level

### Dashboard Outputs

- BMI
- BMR
- TDEE
- Water Intake
- Protein Requirement

### Additional Features

- Food Search
- Food Recommendations
- Macronutrient Analysis
- 3-Month Diet Plan
- AI Diet Assistant

---

# 🛠️ Technology Stack

### Programming Language

- Python

### Libraries

- Pandas
- NumPy
- Scikit-Learn
- Joblib
- Streamlit
- Google Generative AI

### Machine Learning

- Random Forest Classifier

### Frontend

- Streamlit

### AI Assistant

- Google Gemini API

---

# 📂 Project Structure

```text
AI-Personalized-Diet-Recommendation-System/
│
├── datasets/
│   └── raw/
│       │
│       ├── USDA/
│       │   ├── food.csv
│       │   ├── food_nutrient.csv
│       │   └── nutrient.csv
│       │
│       ├── BMI/
│       │   └── bmi.csv
│       │
│       └── daily_nutrition/
│           └── user_nutritional_data.csv
│
├── Cleaned_data/
│   │
│   ├── cleaned_nutrition_dataset.csv
│   │      (food + food_nutrient + nutrient)
│   │
│   ├── cleaned_bmi_dataset.csv
│   │
│   ├── cleaned_calorie_dataset.csv
│   │
│   ├── final_ai_diet_dataset.csv
│   │      (cleaned_nutrition +
│   │       cleaned_bmi +
│   │       cleaned_calorie)
│   │
│   ├── feature_engineered_dataset.csv
│   │
│   └── diet_recommendation_model.pkl
│
├── python/
│   │
│   ├── app.py
│   ├── meal_plan_generator.py
│   ├── gemini_chatbot.py
│   │
│   ├── USDA_Nutrition_Dataset_Cleaning.ipynb
│   ├── bmi_preprocessing.ipynb
│   ├── calorie_preprocessing.ipynb
│   ├── merge_final_dataset.ipynb
│   ├── feature_engineering.ipynb
│   ├── model_training.ipynb
│   └── recommendation_system.ipynb
│
├── outputs/
│   ├── home_page.png
│   ├── recommendation_page.png
│   ├── meal_plan.png
│   └── ai_assistant.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

# 📸 Screenshots

Add your application screenshots inside the `outputs/` folder.

Example:

- Home Page
- Food Recommendations
- Macronutrient Dashboard
- 3-Month Diet Plan
- AI Diet Assistant

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Personalized-Diet-Recommendation-System.git
cd AI-Personalized-Diet-Recommendation-System
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run python/app.py
```

---

# 🔑 Gemini API Setup

This project uses Google Gemini API for the AI Diet Assistant.

## Step 1

Create a folder:

```text
.streamlit
```

## Step 2

Inside the folder create:

```text
secrets.toml
```

## Step 3

Add your API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

## Step 4

Run the application:

```bash
streamlit run python/app.py
```

---

# ℹ️ Important Notes

When the application runs, Python automatically generates cache files:

```text
python/__pycache__/
```

Examples:

```text
gemini_chatbot.cpython-312.pyc
meal_plan_generator.cpython-312.pyc
```

These files are auto-generated by Python and are not required in GitHub repositories.

They are safely ignored using:

```gitignore
__pycache__/
*.pyc
```

---

# 🔮 Future Improvements

- Ranking-based recommendation engine
- Goal-specific meal plans
- Weekly progress tracking
- User authentication
- Cloud deployment
- Advanced nutrition analytics
- Personalized workout planning

---

# 📈 Resume Description

Built an AI-powered Personalized Diet Recommendation System using Machine Learning, USDA FoodData Central nutrition data, Streamlit, and Google Gemini API to generate customized food recommendations, BMI analysis, calorie planning, macronutrient tracking, and a 3-month personalized meal plan based on user health metrics and fitness goals.
