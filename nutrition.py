import streamlit as st
import math

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Smart Body Status Report",
    layout="centered"
)

# =====================================
# STYLE
# =====================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fa;
    color: black;
}

h1 {
    text-align: center;
    color: #2c3e50;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================

st.title("SMART BODY STATUS REPORT")


# =====================================
# INPUTS
# =====================================

name = st.text_input("Enter your name")

gender = st.selectbox(
    "Select your gender",
    ["Female", "Male"]
)

age = st.number_input(
    "Enter your age",
    min_value=10,
    max_value=100
)

height = st.number_input("Height (cm)")
weight = st.number_input("Weight (kg)")

waist = st.number_input("Waist circumference (cm)")
hip = st.number_input("Hip circumference (cm)")
neck = st.number_input("Neck circumference (cm)")

activity = st.selectbox(
    "Select your activity level",
    [
        "Sedentary",
        "Light Activity",
        "Moderate Activity",
        "Very Active",
        "Athlete"
    ]
)

goal = st.selectbox(
    "Select your goal",
    [
        "Lose Fat",
        "Maintain Weight",
        "Gain Muscle"
    ]
)

# =====================================
# ACTIVITY FACTORS
# =====================================

activity_map = {
    "Sedentary": 1.2,
    "Light Activity": 1.375,
    "Moderate Activity": 1.55,
    "Very Active": 1.725,
    "Athlete": 1.9
}

# =====================================
# CALCULATIONS
# =====================================

if st.button("Generate Smart Report"):

    # BMI
    bmi = weight / ((height / 100) ** 2)

    # BMI STATUS
    if bmi < 18.5:
        bmi_status = "Underweight"

    elif bmi < 25:
        bmi_status = "Normal Weight"

    elif bmi < 30:
        bmi_status = "Overweight"

    else:
        bmi_status = "Obesity"

    # =====================================
    # BMR
    # =====================================

    if gender == "Female":
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    else:
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )

    # =====================================
    # TDEE
    # =====================================

    tdee = bmr * activity_map[activity]

    # =====================================
    # GOAL CALORIES
    # =====================================

    if goal == "Lose Fat":
        calories = tdee - 300

    elif goal == "Gain Muscle":
        calories = tdee + 250

    else:
        calories = tdee

    # =====================================
    # WATER
    # =====================================

    water = weight * 0.035

    # =====================================
    # WHR
    # =====================================

    whr = waist / hip

    # =====================================
    # BODY FAT %
    # =====================================

    # Convert cm to inches
    waist_in = waist / 2.54
    hip_in = hip / 2.54
    neck_in = neck / 2.54
    height_in = height / 2.54

    if gender == "Female":

        body_fat = (
            163.205 * math.log10(
                waist_in + hip_in - neck_in
            )
            - 97.684 * math.log10(height_in)
            - 78.387
        )

    else:

        body_fat = (
            86.010 * math.log10(
                waist_in - neck_in
            )
            - 70.041 * math.log10(height_in)
            + 36.76
        )

    # =====================================
    # BODY COMPOSITION
    # =====================================

    fat_mass = weight * (body_fat / 100)

    lean_mass = weight - fat_mass

    # Estimated Skeletal Muscle Mass
    if gender == "Female":
        smm = lean_mass * 0.50

    else:
        smm = lean_mass * 0.55

    # =====================================
    # MACROS
    # =====================================

    protein = weight * 2.2
    fats = weight * 1

    carbs = (
        calories
        - (protein * 4 + fats * 9)
    ) / 4

    # =====================================
    # REPORT
    # =====================================

    st.divider()

    st.header("FINAL BODY REPORT")

    st.write(f"### Name: {name}")
    st.write(f"### Gender: {gender}")
    st.write(f"### Age: {age} years old")

    st.write(f"### Height: {height} cm")
    st.write(f"### Weight: {weight} kg")

    st.divider()

    # =====================================
    # BODY MEASUREMENTS
    # =====================================

    st.subheader("Body Measurements")

    st.write(f"Your BMI is: **{bmi:.1f}**")
    st.write(f"Body Status: **{bmi_status}**")

    st.write(
        f"Estimated Body Fat: "
        f"**{body_fat:.1f}%**"
    )

    st.write(
        f"Estimated Fat Mass: "
        f"**{fat_mass:.1f} kg**"
    )

    st.write(
        f"Lean Body Mass: "
        f"**{lean_mass:.1f} kg**"
    )

    st.write(
        f"Estimated SMM: "
        f"**{smm:.1f} kg**"
    )

    st.write(
        f"Waist-to-Hip Ratio: "
        f"**{whr:.2f}**"
    )

    st.divider()

    # =====================================
    # CALORIES
    # =====================================

    st.subheader("Calories & Energy")

    st.write(
        f"Your BMR is approximately: "
        f"**{bmr:.0f} kcal/day**"
    )

    st.write(
        f"Your daily calories should be approximately: "
        f"**{calories:.0f} kcal/day**"
    )

    st.write(
        f"Based on your activity level: "
        f"**{activity}**"
    )

    st.divider()

    # =====================================
    # WATER
    # =====================================

    st.subheader("Water Intake")

    st.write(
        f"You should drink approximately "
        f"**{water:.1f} liters daily**"
    )

    st.divider()

    # =====================================
    # MACROS
    # =====================================

    st.subheader("Recommended Macronutrients")

    st.write(f"Protein: **{protein:.0f} g**")
    st.write(f"Carbohydrates: **{carbs:.0f} g**")
    st.write(f"Fats: **{fats:.0f} g**")

    st.divider()

    # =====================================
    # RECOMMENDATIONS
    # =====================================

    st.subheader("General Recommendations")

    st.write("• Sleep 7–8 hours daily")
    st.write("• Maintain regular physical activity")
    st.write("• Stay hydrated throughout the day")
    st.write("• Consume enough protein daily")
    st.write("• Include strength training weekly")

    st.divider()

    st.success("Smart Body Report Generated Successfully")