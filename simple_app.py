import streamlit as st
import json
import math
import pandas as pd

st.set_page_config(page_title="Predict Plans", layout="centered")
st.title("תחזית כמות תכניות לפי כמות אדריכליות")

# טען את ה-JSON עם היחסים
with open("mean_ratios.json", "r", encoding="utf-8") as f:
    mean_ratios = json.load(f)

def predict_counts(project_type: str, arch_count: int) -> dict:
    results = {}
    for plan, r in mean_ratios.get(project_type, {}).items():
        # דילוג על inf/NaN
        if not math.isfinite(r):
            continue
        count = round(arch_count * r)
        if count > 0:
            results[plan.replace("ratio_", "")] = count
    return results

# קלט מהמשתמש
project_type = st.selectbox("בחר סוג פרויקט:", list(mean_ratios.keys()))
arch_count = st.number_input("מספר תכניות אדריכליות:", min_value=0, step=1)

if st.button("חשב תחזית"):
    pred = predict_counts(project_type, arch_count)
    if pred:
        df = pd.DataFrame(pred.items(), columns=["תוכנית", "כמות"])
        st.table(df)
    else:
        st.info("אין תחזיות לערכים שהזנת.")
