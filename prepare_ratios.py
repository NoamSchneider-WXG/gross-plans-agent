import json
import pandas as pd

# 1. טען את ה־pivot_df שלך (כאן בדוגמה מ־CSV)
df = pd.read_csv("pivot_df.csv")  # החליפי בשם הקובץ שלך

# 2. חישוב עמודות יחס
plan_cols = [c for c in df.columns if c not in ['pr','thum','אדריכלות']]
for col in plan_cols:
    df[f'ratio_{col}'] = df[col] / df['אדריכלות']

# 3. חישוב ממוצעים לפי סוג פרויקט
ratio_cols = [c for c in df.columns if c.startswith('ratio_')]
grouped = df.groupby('thum')[ratio_cols].mean().reset_index()

# 4. המרת טבלה למילון ושמירה כ-JSON
mean_ratios = grouped.set_index('thum').to_dict(orient='index')
with open("mean_ratios.json", "w", encoding="utf-8") as f:
    json.dump(mean_ratios, f, ensure_ascii=False, indent=2)

print("mean_ratios.json נוצר בהצלחה")
