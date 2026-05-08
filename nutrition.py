import streamlit as st
import math

# =====================================
# 1. PAGE CONFIG & STYLE (التصميم اللي تحبيه)
# =====================================
st.set_page_config(page_title="Smart Body Status Report", layout="centered")

st.markdown("""
<style>
.stApp { background-color: white !important; }
h1, h2, h3, p, label, .stMarkdown, [data-testid="stMarkdownContainer"] { color: black !important; }

/* الزر الأزرق */
div.stButton > button {
    background-color: #007BFF !important;
    color: white !important;
    font-weight: bold !important;
    width: 100%; height: 3.5em;
    border-radius: 10px; border: none; font-size: 18px;
}

/* الدوائر الملونة */
.result-circle {
    border-radius: 50%; width: 110px; height: 110px;
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; margin: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 2. TITLE
# =====================================
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

activity_map = {"Sedentary": 1.2, "Light Activity": 1.375, "Moderate Activity": 1.55, "Very Active": 1.725,
                "Athlete": 1.9}

# =====================================
# 4. CALCULATIONS (المعادلات المنهجية + المعادلة الأمريكية)
# =====================================
if st.button("Generate Report"):

    # [1] BMI (حساب مؤشر كتلة الجسم - أساسي في المنهج)
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # [2] BMR (معادلة ميفلين - أساسية في المنهج)
    if gender == "Female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # [3] TDEE (السعرات المحروقة)
    tdee = bmr * activity_map[activity]

    # تحديد الهدف
    if goal == "Lose Fat":
        calories = tdee - 300
    elif goal == "Gain Muscle":
        calories = tdee + 250
    else:
        calories = tdee

    # [4] Body Fat (معادلة البحرية الأمريكية - الإضافة الدقيقة لمشروعك)
    h_in, w_in, n_in, hp_in = height / 2.54, waist / 2.54, neck / 2.54, hip / 2.54
    try:
        if gender == "Female":
            bf = 163.205 * math.log10(w_in + hp_in - n_in) - 97.684 * math.log10(h_in) - 78.387
        else:
            bf = 86.010 * math.log10(w_in - n_in) - 70.041 * math.log10(h_in) + 36.76
    except:
        bf = 20.0  # قيمة افتراضية في حال الخطأ

    # [5] WHR (نسبة الخصر للحوض - أساسي في المنهج)
    whr = waist / hip
    if gender == "Female":
        whr_status = "Healthy" if whr < 0.85 else "High Risk"
    else:
        whr_status = "Healthy" if whr < 0.90 else "High Risk"

    # [6] Water & Macros (الماء والمغذيات الكبرى)
    water = weight * 0.033
    fat_mass = weight * (bf / 100)
    lean_mass = weight - fat_mass
    protein = weight * 2.0
    fats = weight * 1.0
    carbs = max(0, (calories - (protein * 4 + fats * 9)) / 4)

    # =====================================
    # 5. OUTPUT DISPLAY (التقرير الكامل اللي حبيته)
    # =====================================
    st.divider()
    st.header("✨ FINAL BODY REPORT")

    # الدوائر الثلاث الجمالية
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
            f'<div class="result-circle" style="border: 5px solid #28A745;"><span style="font-size:12px; color:gray;">Kcal</span><b style="font-size:18px; color:#28A745;">{int(calories)}</b></div>',
            unsafe_allow_html=True)

    st.write(f"### Name: {name}")
    st.write(f"**Current Status:** {bmi_status}")

    st.divider()
    st.subheader("📊 Detailed Report")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"BMI: **{bmi:.1f}**")
        st.write(f"Body Fat: **{bf:.1f}%**")
        st.write(f"WHR: **{whr:.2f}** ({whr_status})")
    with col_b:
        st.write(f"Lean Mass: **{lean_mass:.1f} kg**")
        st.write(f"Fat Mass: **{fat_mass:.1f} kg**")
        st.write(f"Water Intake: **{water:.1f} L**")

    st.divider()
    st.subheader("🥗 Energy & Macros")
    st.write(f"Your BMR: **{int(bmr)} kcal**")
    st.write(f"Maintenance (TDEE): **{int(tdee)} kcal**")
    st.write(f"Daily Goal: **{int(calories)} kcal**")

    m1, m2, m3 = st.columns(3)
    m1.metric("Protein", f"{int(protein)}g")
    m2.metric("Carbs", f"{int(carbs)}g")
    m3.metric("Fats", f"{int(fats)}g")

    st.divider()
    st.subheader("💡 Recommendations")
    st.markdown("""
    * Drink plenty of water (at least 2-3 Liters).
    * Focus on whole foods and high-quality protein.
    * Walk at least 10,000 steps daily.
    * Get enough sleep (7-8 hours).
    """)

    st.success("Report generated successfully!")
