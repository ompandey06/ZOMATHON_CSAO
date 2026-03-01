import streamlit as st
import pandas as pd
import json
import os
import random  # Fix for NameError in buttons

# -------------------------------
# 1. Load Data
# -------------------------------


@st.cache_data
def load_data():
    menu_items = pd.read_csv("menu_items.csv")
    rules = pd.read_csv("rules.csv")

    # Clean up stringified lists from CSV
    rules["antecedents"] = rules["antecedents"].apply(json.loads)
    rules["consequents"] = rules["consequents"].apply(json.loads)

    return rules, menu_items


try:
    rules, menu_items = load_data()
    item_info = menu_items.set_index("item_id").to_dict('index')
    item_name_to_id = dict(zip(menu_items["item_name"], menu_items["item_id"]))
except Exception as e:
    st.error(f"⚠️ Error: {e}. Run your notebooks first!")
    st.stop()

# -------------------------------
# 2. UI Styling (Clean & Modern)
# -------------------------------
st.set_page_config(page_title="Zomathon CSAO", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background-color: #cb202d; color: white; font-weight: bold; height: 3em; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("📊 Live Cart Metrics")

st.title("🍴 Zomathon – Smart Cart")
# Team names removed for cleaner UI

# -------------------------------
# 3. Context Selection (Requirement: Contextual Capture)
# -------------------------------
col_a, col_b = st.columns(2)
with col_a:
    meal_time = st.selectbox("🕒 Current Meal Time:", [
                             "Breakfast", "Lunch", "Dinner", "Late Night"])
with col_b:
    user_seg = st.selectbox(
        "👤 User Segment:", ["Regular", "Premium", "Budget"])

selected_names = st.multiselect(
    "🛒 Search & Add Items to Cart:",
    options=menu_items["item_name"].tolist(),
    placeholder="e.g., Royal Biryani, Spicy Burger..."
)

# -------------------------------
# 4. Hybrid Recommendation Engine
# -------------------------------


def get_recommendations(selected_names, current_context):
    if not selected_names:
        return []

    selected_ids = [item_name_to_id[name] for name in selected_names]
    cart_categories = [item_info[iid]['category']
                       for iid in selected_ids if iid in item_info]

    recommendations = []
    seen_items = set(selected_ids)

    # A. Sequential Logic Override (Biryani -> Salan)
    for name in selected_names:
        if "Biryani" in name:
            salan_items = menu_items[menu_items['item_name'].str.contains(
                "Salan")]
            for _, row in salan_items.head(1).iterrows():
                if row['item_id'] not in seen_items:
                    recommendations.append({
                        "item_name": row['item_name'], "category": "Side",
                        "price": row['price'], "score": 10.0,
                        "type": "Next Step in Meal ✨"
                    })
                    seen_items.add(row['item_id'])

    # B. AI-Driven Contextual Rules
    context_rules = rules[rules['context'] == current_context]
    for _, row in context_rules.iterrows():
        if set(row["antecedents"]).issubset(set(selected_ids)):
            for item_id in row["consequents"]:
                if item_id not in seen_items:
                    details = item_info.get(item_id, {})
                    recommendations.append({
                        **details, "score": row["lift"],
                        "type": "Frequently Bought Together ✨"
                    })
                    seen_items.add(item_id)

    # C. Meal Completion Fallback (Beverage)
    if "Main" in cart_categories and "Beverage" not in cart_categories:
        beverages = menu_items[menu_items['category'] == "Beverage"]
        if not beverages.empty:
            for _, row in beverages.sample(n=min(2, len(beverages))).iterrows():
                if row['item_id'] not in seen_items:
                    recommendations.append({
                        "item_name": row['item_name'], "category": "Beverage",
                        "price": row['price'], "score": 1.0, "type": "Complete your meal 🥤"
                    })
                    seen_items.add(row['item_id'])

    return recommendations[:5]


# -------------------------------
# 5. Display Logic
# -------------------------------
if selected_names:
    total_price = sum([item_info[item_name_to_id[name]]['price']
                      for name in selected_names])
    st.sidebar.metric("Current Cart Total", f"₹{total_price}")
    st.sidebar.info(
        "Tip: Adding missing Sides or Drinks completes your meal pattern!")

    st.divider()
    results = get_recommendations(selected_names, meal_time)

    if results:
        st.subheader(f"Recommended for your {meal_time} Order:")
        for rec in results:
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"### {rec['item_name']}")
                    st.write(
                        f"**{rec['type']}** | {rec['category']} | **₹{rec['price']}**")

                    with st.expander("🔍 Why this recommendation?"):
                        # Dynamic explanation based on the recommendation source
                        if rec['type'] == "Next Step in Meal ✨":
                            st.write(
                                f"Our system identified an **Incomplete Meal Pattern**. For a {meal_time} Biryani order, adding a side like {rec['item_name']} is a top user preference.")
                            st.metric("Pattern Priority", "High")
                        else:
                            st.write(
                                f"This item has a strong historical association with your cart during **{meal_time}**.")
                            if 'score' in rec and rec['score'] > 1:
                                st.metric("Lift Score (AI Confidence)",
                                          round(rec['score'], 2))

                with c2:
                    st.write("")
                    # Fixed: Using random for unique keys to prevent NameError
                    st.button(
                        "Add +", key=f"btn_{rec['item_name']}_{random.randint(1,10000)}")
                st.divider()
else:
    st.info("Start adding items like 'Biryani' or 'Pasta' to see smart suggestions!")
