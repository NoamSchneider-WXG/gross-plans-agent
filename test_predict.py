import json
import math

# טען את ה-JSON של היחסים
with open("mean_ratios.json", "r", encoding="utf-8") as f:
    mean_ratios = json.load(f)

def predict_counts(project_type: str, arch_count: int) -> dict:
    """
    מחזיר dict של {'תוכנית': כמות_תחזית} לפי mean_ratios,
    מסנן ערכים לא חוקיים (inf, NaN) ויחסים שמניבים <=0.
    """
    ratios = mean_ratios.get(project_type, {})
    results = {}
    for plan, r in ratios.items():
        # התעלם אם היחס לא סופי (inf או NaN)
        if not math.isfinite(r):
            continue
        count = arch_count * r
        # רק מספרים חיוביים
        if count > 0:
            results[plan.replace("ratio_", "")] = int(round(count))
    return results

if __name__ == "__main__":
    # כאן תגדירי מקרים לבדיקה
    tests = [
        ("מגורים", 10),
        ("משרדים", 5),
        ("תעשיה", 8),
    ]

    for project_type, arch_count in tests:
        pred = predict_counts(project_type, arch_count)
        print(f"> פרויקט='{project_type}', אדריכלות={arch_count} → {pred}")
