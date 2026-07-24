import os
import streamlit as st
import pandas as pd
import joblib
from gemini_chatbot import ask_gemini
from meal_plan_generator import generate_meal_plan

# =====================================================
# BASE DIRECTORY & FILE PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "Cleaned_data", "feature_engineered_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "Cleaned_data", "diet_recommendation_model.pkl")

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Diet Recommendation System",
    page_icon="🥗",
    layout="wide"
)


st.markdown(
    """
    <div class="main-title-container"></div>
    """,
    unsafe_allow_html=True
)


page_bg = """
<style>

/* MAIN BACKGROUND */

[data-testid="stAppViewContainer"] {
    background-color: #000000;
    color: white;
}

/* TOP IMAGE BANNER */

.main-title-container {
    background-image: url("https://www.eatingwell.com/thmb/YxkWBfh2AvNYrDKoHukRdmRvD5U=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/article_291139_the-top-10-healthiest-foods-for-kids_-02-4b745e57928c4786a61b47d8ba920058.jpg");
    
    background-size: cover;
    background-position: center;

    height: 280px;
    border-radius: 20px;
    margin-bottom: 25px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: #111111;
}

/* TEXT COLOR */

h1, h2, h3, h4, h5, h6,
p, label, div, span {
    color: white !important;
}

/* METRIC CARDS */

.stMetric {

    background-color: #1e1e1e;

    padding: 15px;

    border-radius: 15px;

    border: 1px solid #333333;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {

    background-color: #111111;

    border-radius: 15px;
}

/* BUTTONS */

.stButton>button {

    background-color: #00c853;

    color: white;

    border-radius: 10px;

    border: none;

    font-weight: bold;
}

/* DOWNLOAD BUTTON */

.stDownloadButton>button {

    background-color: #ff9800;

    color: white;

    border-radius: 10px;

    border: none;
}

/* INPUT BOXES */

.stTextInput input,
.stNumberInput input {

    background-color: #1e1e1e;

    color: white;
}

/* SLIDER */

.stSlider {
    color: white;
}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv(DATASET_PATH)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(MODEL_PATH)


# =====================================================
# cleaniing food colums
# =====================================================
import re

def clean_food_name(food):
    
    food = str(food)

    # Remove "(0% moisture)"
    food = re.sub(r"\s*\(.*?moisture.*?\)", "", food)

    # Remove codes like 11F-8081, 510, 299, 315
    food = re.sub(r",\s*[A-Z0-9\-]+$", "", food)

    # Remove trailing numbers
    food = re.sub(r",\s*\d+$", "", food)

    return food.strip()

df["food"] = df["food"].apply(clean_food_name)


# =====================================================
# LABEL MAPPING
# =====================================================

goal_mapping = {
    0: "Average",
    1: "Weight Gain",
    2: "Weight Loss"
}


def calculate_bmr(gender, weight, height, age):

    if gender == 1:  # Male

        bmr = (
            10 * weight +
            6.25 * height -
            5 * age +
            5
        )

    else:  # Female

        bmr = (
            10 * weight +
            6.25 * height -
            5 * age -
            161
        )

    return round(bmr, 2)

# =====================================================
# RECOMMENDATION FUNCTION
# =====================================================

def recommend_foods(
    gender,
    age,
    height,
    weight,
    meals_per_day,
    bmr,
    tdee
):
    
    # BMI
    height_m = height / 100

    bmi = weight / (height_m ** 2)

    # Daily requirements
    water_intake = round(weight * 0.033, 2)

    protein_need = round(weight * 1.6, 2)

    # Model input
    input_data = pd.DataFrame({

        'gender': [gender],

        'height': [height],

        'weight': [weight],

        'age': [age],

        'bmi': [bmi],

        'meals_per_day': [meals_per_day],

        'bmr': [bmr],

        'water_intake_liters': [water_intake],

        'daily_protein_need': [protein_need]

    })

        # Prediction
    # =================================================
    # BMI-BASED FITNESS GOAL SYSTEM
    # =================================================

    if bmi < 18.5:

        goal = "Thin"

        recommendations = df[
            df['calories'] > 500
        ]

    elif bmi < 23:

        goal = "Medium"

        recommendations = df[
            df['calories'] > 1500
        ]

    elif bmi < 27:

        goal = "Fit"

        recommendations = df[
            df['protein'] > 15
        ]

    else:

        goal ="Advance Fit"

        recommendations = df[
            df['protein'] > 25
        ]

    # =================================================
    # CLEAN RECOMMENDATIONS
    # =================================================

    recommendations = recommendations[
        recommendations['food'].notna()
    ]

    recommendations = recommendations.drop_duplicates(  
        subset=['food']
    )

    # =================================================
    # RANDOM FOODS
    # =================================================

    recommendations = recommendations.drop_duplicates(
        subset=['food']
    )


    # ==========================================
    # PERSONALIZED FOOD SCORING
    # ==========================================

    target_calories = tdee / meals_per_day

    target_protein = protein_need / meals_per_day

    recommendations["score"] = (

    abs(
        recommendations["calories"]
        - target_calories
    ) * 0.5

    +

    abs(
        recommendations["protein"]
        - target_protein
    ) * 2

)

    recommendations = (

        recommendations

        .sort_values(
            by="score"
        )

        .head(10)

    )

    # Important columns
    recommendations = recommendations[
        [
            'food',
            'calories',
            'protein',
            'carbs',
            'fat',
            'fiber'
        ]
    ]

    return (
        goal,
        round(bmi, 2),
        water_intake,
        protein_need,
        recommendations
    )


# =====================================================
# TITLE
# =====================================================

st.title("🥗 AI Personalized Diet Recommendation System")

st.markdown("""
### Get AI-powered food recommendations based on:
- BMI (Body Mass Index)
- Calories
- Protein Needs
- Fitness Goals
- BMR (Basal Metabolic Rate)
- Daily Calories (TDEE)
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Enter Your Details")

# Gender
gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

gender_value = 1 if gender == "Male" else 0

# Age
age = st.sidebar.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=24
)

# Height
height = st.sidebar.number_input(
    "Height (cm)",
    min_value=100,
    max_value=250,
    value=170
)

# Weight
weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=20,
    max_value=250,
    value=70
)

# Meals
meals_per_day = st.sidebar.slider(
    "Meals Per Day",
    1,
    10,
    3
)

activity_level = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Extremely Active"
    ]
)

def calculate_tdee(bmr, activity_level):

    activity_factors = {

        "Sedentary": 1.2,

        "Lightly Active": 1.375,

        "Moderately Active": 1.55,

        "Very Active": 1.725,

        "Extremely Active": 1.9
    }

    return round(
        bmr * activity_factors[activity_level],
        2
    )

# =====================================================
# GENERATE BUTTON
# =====================================================

if st.sidebar.button("Generate Recommendation"):

    bmr = calculate_bmr(
        gender_value,
        weight,
        height,
        age
    )

    tdee = calculate_tdee(
        bmr,
        activity_level
    )

    goal, bmi, water, protein, foods = recommend_foods(
        gender=gender_value,
        age=age,
        height=height,
        weight=weight,
        meals_per_day=meals_per_day,
        bmr=bmr,
        tdee=tdee
    )

    st.session_state.goal = goal
    st.session_state.bmi = bmi
    st.session_state.water = water
    st.session_state.protein = protein
    st.session_state.foods = foods
    st.session_state.bmr = bmr
    st.session_state.tdee = tdee
    st.session_state.generated = True

# ==========================================
# LOAD SAVED RESULTS
# ==========================================

if st.session_state.get("generated", False):

    goal = st.session_state.goal

    bmi = st.session_state.bmi

    water = st.session_state.water

    protein = st.session_state.protein

    foods = st.session_state.foods

    bmr = st.session_state.bmr

    tdee = st.session_state.tdee


    foods = foods[
    foods["food"].notna()
]

    foods = foods[
        foods["food"].str.len() > 5
    ]

    foods = foods[
        ~foods["food"].str.contains(
            "raw|inedible|refuse",
            case=False,
            na=False
        )
    ]



    # =================================================
    # GOAL
    # =================================================

    st.success(f"🎯 Recommended Goal: {goal}")

    # =================================================
    # BMI STATUS
    # =================================================

    if bmi < 18.5:

        st.warning("⚠️ You are Underweight")

    elif bmi < 25:

        st.success("✅ You are Healthy")

    elif bmi < 30:

        st.warning("⚠️ You are Overweight")

    else:

        st.error("🚨 Obesity Risk")

    # =================================================
    # METRICS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "BMI",
            bmi
        )

    with col2:

        st.metric(
            "Daily Water Intake",
            f"{water} L"
        )

    with col3:

        st.metric(
            "Daily Protein Need",
            f"{protein} g"
        )
    col4, col5 = st.columns(2)

    with col4:

        st.metric(
            "BMR",
            round(bmr)
        )

    with col5:

        st.metric(
            "Daily Calories (TDEE)",
            round(tdee)
        )

        
    # =================================================
    # BMI PROGRESS BAR
    # =================================================

    st.subheader("BMI Indicator")

    st.progress(min(int(bmi * 4), 100))

    # =================================================
    # FOOD SEARCH
    # =================================================
    foods_original = foods.copy()

    st.subheader("🔍 Search Food")

    with st.form("search_form"):

        food_search = st.text_input(
            "Type food name"
        )

        search_button = st.form_submit_button(
            "Search"
        )

    if search_button and food_search:

        search_results = df[
            df["food"]
            .fillna("")
            .str.contains(
                food_search,
                case=False,
                na=False
            )
        ]

        st.subheader("Search Results")

        st.dataframe(
            search_results[
                [
                    "food",
                    "calories",
                    "protein",
                    "carbs",
                    "fat",
                    "fiber"
                ]
            ].head(20)
        )

        if foods.empty:
            st.warning("No foods found for this search.")
    # =================================================
    # FOOD TABLE
    # =================================================

    st.subheader("🍎 Recommended Foods")

    st.dataframe(
        foods,
        use_container_width=True
    )

    # =================================================
    # 3-Month Personalized Diet Plan
    # =================================================
    st.subheader("📅 3-Month Personalized Diet Plan")

    if foods_original.empty:
        st.error("No foods available to generate meal plan.")
        st.stop()

    meal_plan = generate_meal_plan(
        foods_original,
        goal,
        round(tdee)
    )
    selected_week = st.selectbox(
        "Select Week",
        list(range(1, 13))
    )

    start_idx = (selected_week - 1) * 7
    end_idx = start_idx + 7

    week_plan = meal_plan.iloc[
        start_idx:end_idx
    ]

    st.dataframe(
        week_plan,
        use_container_width=True
    )

    # ===================================
    # DOWNLOAD FULL 3 MONTH PLAN
    # ===================================

    csv_plan = meal_plan.to_csv(
        index=False
    )

    st.download_button(

        "📥 Download 3-Month Diet Plan",

        csv_plan,

        "3_month_diet_plan.csv",

        "text/csv"
    )


    # =================================================
    # CHART
    # =================================================

    st.subheader("📊 Macronutrient Comparison")

    if not foods.empty:

        chart_data = foods[
            ['protein', 'carbs', 'fat']
        ]

        st.bar_chart(chart_data)

    else:

        st.warning("No foods found.")
        
    chart_data = foods[
        ['protein', 'carbs', 'fat']
    ]

    # st.bar_chart(chart_data)

    # =================================================
    # HEALTH SUMMARY
    # =================================================

    st.info(f"""
    Daily Health Summary

    • BMI: {bmi}

    • Water Intake: {water} Liters

    • Protein Requirement: {protein} grams

    • Goal: {goal}
    """)

    # =================================================
    # DOWNLOAD BUTTON
    # =================================================

    csv = foods.to_csv(index=False)

    st.download_button(

        label="📥 Download Recommendations",

        data=csv,

        file_name="diet_recommendations.csv",

        mime="text/csv"
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")


# ============================================
# DEFAULT VALUES FOR CHATBOT
# ============================================

bmr = calculate_bmr(
    gender_value,
    weight,
    height,
    age
)

tdee = calculate_tdee(
    bmr,
    activity_level
)

height_m = height / 100

bmi = round(
    weight / (height_m ** 2),
    2
)

water = round(
    weight * 0.033,
    2
)

protein = round(
    weight * 1.6,
    2
)

# Goal Calculation

if bmi < 18.5:

    goal = "Thin"

elif bmi < 23:

    goal = "Medium"

elif bmi < 27:

    goal = "Fit"

else:

    goal = "Advance Fit"

# =====================================================
# AI FITNESS CHATBOT
# =====================================================
st.markdown("---")
st.subheader("🤖 AI Diet Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

question = st.chat_input(
    "Ask me anything about diet, fitness, nutrition..."
)
if question:

    prompt = f"""
    You are an expert nutritionist and fitness coach.

    User Details:

    Age: {age}
    Gender: {gender}
    Height: {height} cm
    Weight: {weight} kg
    BMI: {bmi}
    Water Intake Recommendation: {water} liters
    Daily Protein Requirement: {protein} grams
    Fitness Goal: {goal}

    BMR: {bmr}

    TDEE: {tdee}

    Activity Level: {activity_level}

    User Question:
    {question}

    You are an expert AI nutritionist.

Give detailed personalized advice.

Include:
1. Explanation
2. Recommended foods
3. Foods to avoid
4. Water recommendation
5. Exercise recommendation

Keep response under 200 words.
    """

    answer = ask_gemini(prompt)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    st.chat_message("user").write(question)

    st.chat_message("assistant").write(answer)
if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()
    




