import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 🎮 Game Introduction
# ------------------------------

st.title("🏗️ Green Building Transformation: Sustainable Industry Simulation Game")

st.markdown("""
## 📌 Achieving Energy Efficiency with Recycled Materials & PCM
### 🎯 Goal:
Reduce cooling loads and optimize energy efficiency in building enclosures using **Recycled Waste Paper (RWP) and Phase Change Materials (PCM)**.

---
### 🏢 **Background**
You are the **Sustainability Director** of **EcoBuild Innovations**.  
Your mission: **Implement sustainable building materials** to cut **cooling load by 30%** while staying **within budget**.

### 🚀 **Key Challenges**
1. **Reduce Cooling Load & Electricity Costs** 📉  
2. **Optimize Material Sustainability & Noise Insulation** 🌱🔇  
3. **Manage a $10M Budget Effectively** 💰  

---
## 📅 Yearly Decision Process
Each year, choose **up to 3 sustainability initiatives**.  
Each decision affects **cost, cooling load reduction, & energy savings**.

| **Initiative** | **Cooling Load Reduction** | **Cost** | **Implementation Time** |
|--------------|-----------|----------|----------------|
| **25% RWP + PCM Walls** 🏗️ | -5% | $2M | 1 Year |
| **50% RWP + PCM Walls** 🏠 | -10% | $3.5M | 2 Years |
| **75% RWP + PCM Walls** 🌿 | -15% | $5M | 3 Years |
| **PCM Integrated Roof Coating** ☀️ | -7% | $2M | 2 Years |
| **IoT-Based Energy Monitoring** 📊 | -5% Energy Use | $1.5M | 1 Year |
| **Advanced Acoustic Panels** 🔇 | +7% Noise Reduction | $1M | 1 Year |
| **Hybrid Ventilation System** 🌬️ | -6% | $3M | 2 Years |
| **Automated Insulation Adjustments** ⚙️ | -4% | $2.5M | 1 Year |

---
""")

st.sidebar.header("Game Settings")
years = st.sidebar.slider("Select Simulation Years", min_value=3, max_value=7, value=5)

# ------------------------------
# 🎯 Game Configuration
# ------------------------------
initiatives = {
    "25% RWP + PCM Walls": {"Cooling Load Reduction": 5, "Cost": 2, "Implementation Years": 1},
    "50% RWP + PCM Walls": {"Cooling Load Reduction": 10, "Cost": 3.5, "Implementation Years": 2},
    "75% RWP + PCM Walls": {"Cooling Load Reduction": 15, "Cost": 5, "Implementation Years": 3},
    "PCM Integrated Roof Coating": {"Cooling Load Reduction": 7, "Cost": 2, "Implementation Years": 2},
    "IoT-Based Energy Monitoring": {"Cooling Load Reduction": 5, "Cost": 1.5, "Implementation Years": 1},
    "Advanced Acoustic Panels": {"Noise Reduction": 7, "Cost": 1, "Implementation Years": 1},
    "Hybrid Ventilation System": {"Cooling Load Reduction": 6, "Cost": 3, "Implementation Years": 2},
    "Automated Insulation Adjustments": {"Cooling Load Reduction": 4, "Cost": 2.5, "Implementation Years": 1},
}

# Initial settings
starting_cooling_load = 100  # Initial cooling load (percentage of baseline)
cooling_reduction_target = 30  # Target reduction percentage
initial_budget = 10  # Initial budget in $M

# ------------------------------
# 🏁 Implementing Session State for Persistence
# ------------------------------
if "game_data" not in st.session_state:
    st.session_state.game_data = {
        "Year": [],
        "Chosen Initiatives": [],
        "Cooling Load Reduction": [],
        "Total Cost": [],
        "Remaining Budget": [],
    }

# ------------------------------
# 📅 Yearly Decision Process
# ------------------------------
st.header("📅 Yearly Decision-Making")

for year in range(1, years + 1):
    st.subheader(f"Year {year}")

    selected_initiatives = st.multiselect(
        f"Select up to 3 initiatives for Year {year}",
        list(initiatives.keys()),
        default=[],
        max_selections=3,
    )

    if st.button(f"Confirm Choices for Year {year}"):
        if not selected_initiatives:
            st.warning("Please select at least one initiative.")
        else:
            total_cooling_reduction = sum(initiatives[c]["Cooling Load Reduction"] for c in selected_initiatives if "Cooling Load Reduction" in initiatives[c])
            total_cost = sum(initiatives[c]["Cost"] for c in selected_initiatives)

            # Ensure the budget is updated correctly
            budget_left = (
                st.session_state.game_data["Remaining Budget"][-1] - total_cost
                if len(st.session_state.game_data["Remaining Budget"]) > 0
                else initial_budget - total_cost
            )

            # Append data correctly to match list lengths
            st.session_state.game_data["Year"].append(year)
            st.session_state.game_data["Chosen Initiatives"].append(selected_initiatives)
            st.session_state.game_data["Cooling Load Reduction"].append(total_cooling_reduction)
            st.session_state.game_data["Total Cost"].append(round(total_cost, 2))
            st.session_state.game_data["Remaining Budget"].append(round(budget_left, 2))

            st.success(f"Year {year} decisions saved! See results below.")

    st.write("---")

# ------------------------------
# 📊 Results & Visualization
# ------------------------------
if len(st.session_state.game_data["Year"]) > 0:
    df_results = pd.DataFrame(st.session_state.game_data)

    # Ensure cumulative Cooling Load Reduction is tracked correctly
    df_results["Cumulative_Cooling_Reduction"] = df_results["Cooling Load Reduction"].cumsum()
    df_results["Remaining_Cooling_Load"] = starting_cooling_load - df_results["Cumulative_Cooling_Reduction"]

    st.header("📊 Game Summary")
    st.write(df_results)

    # Score Calculation
    cooling_score = min(30, df_results["Cumulative_Cooling_Reduction"].iloc[-1] / cooling_reduction_target * 30)
    budget_score = 10 if df_results["Remaining Budget"].iloc[-1] > 0 else 0

    total_score = cooling_score + budget_score
    st.subheader(f"🏆 **Final Score: {total_score}/100**")

    # Cooling Load Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_results["Year"], df_results["Remaining_Cooling_Load"], marker="o", linestyle="-", label="Cooling Load Reduction")

    ax.set_xlabel("Year")
    ax.set_ylabel("Cooling Load (% of baseline)")
    ax.set_title("Cooling Load Reduction Over Time")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    if total_score >= 80:
        st.success("🎉 Congratulations! Your buildings are highly sustainable! 🎉")
    elif total_score >= 50:
        st.warning("⚠️ Good progress, but more improvements are needed.")
    else:
        st.error("❌ You failed to meet sustainability goals.")
