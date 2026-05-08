import streamlit as st
import math

# =====================================
# 1. PAGE CONFIG & STYLE
# =====================================
st.set_page_config(page_title="Smart Body Status Report", layout="centered")

st.markdown("""
<style>
.stApp { background-color: white !important; }
h1, h2, h3, p, label, .stMarkdown, [data-testid="stMarkdownContainer"] { color: black !important; }
div.stButton > button {
    background-color: #007BFF !important;
    color: white !important;
    font-weight: bold !important;
    width: 100%; height: 3.5em;
    border-radius: 10px; border: none; font-size: 18px;
}
.result-circle {
    border-radius: 50%; width: 110px; height: 110px;
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; margin: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: white;
}
.accuracy-box {
    color: #28A745;
    font-weight: bold;
    font-size: 20px;
    border: 2px solid #28A745;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("SMART BODY STATUS REPORT")

# =====================================
# 3. INPUTS
# =====================================
name = st.text_input("Enter your name")
gender = st.selectbox("Select gender", ["Female", "Male"])
age = st.number_input("Age", 10, 100, 25)

col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Height (cm)", 100.0, 250.0, 160.0)
    waist = st.number_input("Waist (cm)", 20.0, 200.0, 70.0)
with col2:
    weight = st.number_input("Weight (kg)", 20.0, 300.0, 60.0)
    hip = st.number_input("Hip (cm)", 20.0, 200.0, 90.0)

neck = st.number_input("Neck (cm)", 10.0, 100.0, 35.0)
activity = st.selectbox("Activity level",
                        ["Sedentary", "Light Activity", "Moderate Activity", "Very Active", "Athlete"])
goal = st.selectbox("Goal", ["Lose Fat", "Maintain Weight", "Gain Muscle"])

# =====================================
# 4. CALCULATIONS
# =====================================
if st.button("Generate Report"):
    # [1] BMI & BMR
    bmi = weight / ((height / 100) ** 2)
    if gender == "Female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # [2] Body Fat (Hybrid Stability)
    h_in, w_in, n_in, hp_in = height / 2.54, waist / 2.54, neck / 2.54, hip / 2.54
    try:
        if gender == "Female":
            bf_n = 163.205 * math.log10(w_in + hp_in - n_in) - 97.684 * math.log10(h_in) - 78.387
        else:
            bf_n = 86.010 * math.log10(w_in - n_in) - 70.041 * math.log10(h_in) + 36.76
        if bf_n < 3 or bf_n > 55: raise ValueError
    except:
        bf_n = None

    g_val = 0 if gender == "Female" else 1
    bf_bmi = (1.20 * bmi) + (0.23 * age) - (10.8 * g_val) - 5.4
    bf = (0.7 * bf_n + 0.3 * bf_bmi) if bf_n is not None else bf_bmi

    # [3] Athlete & Muscle Detection
    lean_mass = weight * (1 - (bf / 100))
    lean_ratio = lean_mass / weight
    threshold = 0.72 if gender == "Female" else 0.82
    muscular_flag = (lean_ratio > threshold and bmi > (21 if gender == "Female" else 23))
    is_athletic = (bmi >= 25 and lean_ratio > (threshold - 0.02)) or activity == "Athlete"

    # [4] Energy (TDEE) & Goal Adjustment
    act_map = {"Sedentary": 1.2, "Light Activity": 1.375, "Moderate Activity": 1.55, "Very Active": 1.725,
               "Athlete": 1.9}
    scientific_tdee = bmr * act_map[activity]

    # Moderate Adjustment for Athletes (Stable Layer)
    met_adj = 1.0 if is_athletic else (0.97 if bf > 32 else 1.0)

    if goal == "Lose Fat":
        base_cal = scientific_tdee - 400
    elif goal == "Gain Muscle":
        base_cal = scientific_tdee + 250
    else:
        base_cal = scientific_tdee

    final_calories = base_cal * met_adj
    cal_min, cal_max = final_calories * 0.95, final_calories * 1.05

    # [5] Macro Distribution (RE-TUNED to fix high fats)
    protein = lean_mass * 2.3 if is_athletic else weight * 2.0

    # Fat Logic: Tuned down to avoid the 73g issue
    if bf > 30:
        fat_ratio = 0.18  # Low fat for higher BF
    elif is_athletic:
        fat_ratio = 0.22  # Perfect balance for athletes
    else:
        fat_ratio = 0.20  # Standard

    fats = (final_calories * fat_ratio) / 9
    carbs = (final_calories - (protein * 4 + fats * 9)) / 4

    # [6] Confidence Score
    conf = 0.85
    if 18.5 < bmi < 26: conf += 0.05
    if bf > 45 or bf < 6: conf -= 0.10
    conf = max(0.5, min(0.97, conf))

    # =====================================
    # 5. OUTPUT DISPLAY
    # =====================================
    st.divider()
    st.header(f"FINAL REPORT FOR {name.upper()}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="result-circle" style="border: 5px solid #007BFF;"><span style="font-size:12px; color:gray;">BMI</span><b style="font-size:20px; color:#007BFF;">{bmi:.1f}</b></div>',
            unsafe_allow_html=True)
    with c2:
        st.markdown(
            f'<div class="result-circle" style="border: 5px solid #FF4B4B;"><span style="font-size:12px; color:gray;">Fat %</span><b style="font-size:20px; color:#FF4B4B;">{bf:.1f}%</b></div>',
            unsafe_allow_html=True)
    with c3:
        st.markdown(
            f'<div class="result-circle" style="border: 5px solid #28A745;"><span style="font-size:10px; color:gray;">Kcal Range</span><b style="font-size:14px; color:#28A745;">{int(cal_min)}-{int(cal_max)}</b></div>',
            unsafe_allow_html=True)

    # Status & Accuracy
    st.markdown(f'<div class="accuracy-box">Report Confidence Score: {conf * 100:.0f}%</div>', unsafe_allow_html=True)

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Normal"
    elif muscular_flag or is_athletic:
        status = "Athletic / Muscular"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    st.info(f"**Current Status:** {status}")
    if muscular_flag or is_athletic:
        st.warning(
            "⚠️ **Note:** For athletic individuals, BMI might be inaccurate as it does not distinguish between muscle and fat mass.")

    st.divider()

    # Detailed Report
    st.subheader("📊 Detailed Report")
    whr = waist / hip
    whr_status = "(Healthy)" if (gender == "Female" and whr <= 0.85) or (
            gender == "Male" and whr <= 0.90) else "(High Risk)"

    # الحسابات (تتم خلف الكواليس)
    estimated_muscle_kg = lean_mass * 0.82
    muscle_percentage = (estimated_muscle_kg / weight) * 100

    col_a, col_b = st.columns(2)

    with col_a:
        st.write(f"BMI: **{bmi:.1f}**")
        st.write(f"Body Fat: **{bf:.1f}%**")
        st.write(f"Muscle Percentage: **{muscle_percentage:.1f}%**")  # نقلناها هنا للتوازن
        st.write(f"WHR: **{whr:.2f} {whr_status}**")

    with col_b:
        st.write(f"Lean Mass: **{lean_mass:.1f} kg**")
        st.write(f"Muscle Mass: **{estimated_muscle_kg:.1f} kg**")  # العضل بالكيلو
        st.write(f"Fat Mass: **{weight - lean_mass:.1f} kg**")
        st.write(f"Water Intake: **{weight * 0.035:.1f} L**")

    st.divider()

    # Energy & Macros
    st.subheader("🥗 Energy & Macros")
    st.write(f"Your BMR: **{int(bmr)} kcal**")
    st.write(f"Maintenance (TDEE): **{int(scientific_tdee)} kcal**")
    st.write(f"Daily Goal (Smart Adjusted): **{int(final_calories)} kcal**")

    # توزيع الماكروس في أعمدة بنفس ستايل الدوائر العلوية
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f'<div class="result-circle" style="border: 5px solid #007BFF;">'
            f'<span style="font-size:12px; color:gray;">Protein</span>'
            f'<b style="font-size:20px; color:#007BFF;">{int(protein)}g</b>'
            f'</div>', unsafe_allow_html=True)

    with m2:
        st.markdown(
            f'<div class="result-circle" style="border: 5px solid #FFA500;">'
            f'<span style="font-size:12px; color:gray;">Carbs</span>'
            f'<b style="font-size:20px; color:#FFA500;">{int(carbs)}g</b>'
            f'</div>', unsafe_allow_html=True)

    with m3:
        st.markdown(
            f'<div class="result-circle" style="border: 5px solid #6C757D;">'
            f'<span style="font-size:12px; color:gray;">Fats</span>'
            f'<b style="font-size:20px; color:#6C757D;">{int(fats)}g</b>'
            f'</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("💡 Recommendations")
    st.write("1. Drink 2-3L of water daily.")
    st.write("2. Focus on high-quality protein and whole carbs.")
    st.write("3. Keep active and monitor trends over time.")
    st.write("4. don't forget to rest your body for better recovery")

    st.success("Analysis complete.")