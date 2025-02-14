import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 🎮 Game Introduction
# ------------------------------

st.title("🏭 Kalundborg Eco-Industrial Park Simulation Game")

st.markdown("""
## 📌 Industrial Symbiosis at Kalundborg: A Circular Economy Challenge
### 🎯 Goal:
As the **Sustainability Manager**, optimize **waste reuse, CO₂ reduction, and financial sustainability** by making **strategic decisions** over a **5-year period**.

---
### 🏢 **Background**
Kalundborg, Denmark, hosts **the world’s most renowned eco-industrial network**.  
Your mission: **Expand this symbiosis model while ensuring environmental & financial success**.

### 🚀 **Key Challenges**
1. **Reduce CO₂ Emissions & Optimize Resource Sharing** ♻️  
2. **Balance Financial Investments** 💰 **(Starting Budget: $50M)**  
3. **Maintain Regulatory & Stakeholder Satisfaction** 🏆  

---
## 📅 Yearly Decision Process
Each year, choose **up to 3 sustainability initiatives**.  
Each decision impacts **CO₂ emissions, financial performance, and eco-industrial symbiosis**.

| **Initiative** | **CO₂ Reduction** | **Cost** | **Implementation Time** |
|--------------|-----------|----------|----------------|
| **Waste Heat Exchange System** 🔥 | -10% | $10M | 2 Years |
| **Water Recycling Infrastructure** 💧 | -15% Freshwater Use | $12M | 3 Years |
| **Biomass Energy Integration** 🌿 | -12% | $15M | 3 Years |
| **Carbon Capture & Storage (CCS)** 🌫️ | -20% | $18M | 5 Years |
| **By-Product Sharing (Gypsum, Sulfur, Sludge)** ♻️ | -8% Waste Disposal Costs | $7M | 2 Years |
| **AI-Optimized Resource Allocation** 🤖 | -5% Operating Costs | $5M | 1 Year |
| **New Industry Partner Expansion** 🏭 | +20% Industrial Output | $20M | 4 Years |
| **Public Awareness & ESG Branding** 📢 | +10% Stakeholder Approval | $3M | 1 Year |

---
""")

st.sidebar.header("Game Settings")
years = st.sidebar.slider("Select Simulation Years", min_value=3, max_value=7, value=5)

# ------------------------------
# 🎯 Game Configuration
# ------------------------------
initiatives = {
    "Waste Heat Exchange System": {"CO2 Reduction": 10, "Cost": 10, "Implementation Years": 2},
    "Water Recycling Infrastructure": {"CO2 Reduction": 15, "Cost": 12, "Implementation Years": 3},
    "Biomass Energy Integration": {"CO2 Reduction": 12, "Cost": 15, "Implementation Years": 3},
    "Carbon Capture & Storage (CCS)": {"CO2 Reduction": 20, "Cost": 18, "Implementation Years": 5},
    "By-Product Sharing (Gypsum, Sulfur, Sludge)": {"CO2 Reduction": 8, "Cost": 7, "Implementation Years": 2},
    "AI-Optimized Resource Allocation": {"CO2 Reduction": 5, "Cost": 5, "Implementation Years": 1},
    "New Industry Partner Expansion": {"CO2 Reduction": 0, "Cost": 20, "Implementation Years": 4},
    "Public Awareness & ESG Branding": {"CO2 Reduction": 0, "Cost": 3, "Implementation Years": 1},
}

# Initial settings
starting_co2 = 100  # Initial CO2 level (percentage of baseline)
co2_reduction_target = 40  # Target CO2 reduction percentage
initial_budget = 50  # Initial budget in $M

# ------------------------------
# 🏁 Implementing Session State for Persistence
# ------------------------------
if "game_data" not in st.session_state:
    st.session_state.game_data = {
        "Year": [],
        "Chosen Initiatives": [],
        "CO2 Reduction": [],
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
            total_co2_reduction = sum(initiatives[c]["CO2 Reduction"] for c in selected_initiatives)
            total_cost = sum(initiatives[c]["Cost"] for c in selected_initiatives)

            budget_left = (
                st.session_state.game_data["Remaining Budget"][-1] - total_cost
                if len(st.session_state.game_data["Remaining Budget"]) > 0
                else initial_budget - total_cost
            )

            st.session_state.game_data["Year"].append(year)
            st.session_state.game_data["Chosen Initiatives"].append(selected_initiatives)
            st.session_state.game_data["CO2 Reduction"].append(total_co2_reduction)
            st.session_state.game_data["Total Cost"].append(round(total_cost, 2))
            st.session_state.game_data["Remaining Budget"].append(round(budget_left, 2))

            st.success(f"Year {year} decisions saved! See results below.")

    st.write("---")

# ------------------------------
# 📊 Results & Visualization
# ------------------------------
if len(st.session_state.game_data["Year"]) > 0:
    df_results = pd.DataFrame(st.session_state.game_data)
    df_results["Cumulative_CO2_Reduction"] = df_results["CO2 Reduction"].cumsum()
    df_results["Remaining_CO2"] = starting_co2 - df_results["Cumulative_CO2_Reduction"]

    st.header("📊 Game Summary")
    st.write(df_results)

    # Score Calculation
    co2_score = min(30, df_results["Cumulative_CO2_Reduction"].iloc[-1] / co2_reduction_target * 30)
    budget_score = 10 if df_results["Remaining Budget"].iloc[-1] > 5 else 0
    stakeholder_score = 15 if "Public Awareness & ESG Branding" in st.session_state.game_data["Chosen Initiatives"] else 5
    industry_growth_score = 15 if "New Industry Partner Expansion" in st.session_state.game_data["Chosen Initiatives"] else 5
    total_score = co2_score + budget_score + stakeholder_score + industry_growth_score

    st.subheader(f"🏆 **Final Score: {total_score}/100**")

    # CO2 Reduction Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_results["Year"], df_results["Remaining_CO2"], marker="o", linestyle="-", label="CO2 Reduction")

    ax.set_xlabel("Year")
    ax.set_ylabel("CO2 Emissions (% of baseline)")
    ax.set_title("CO2 Emission Reduction Over Time")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    if total_score >= 80:
        st.success("🎉 Congratulations! Your industrial symbiosis model is a success!")
    elif total_score >= 50:
        st.warning("⚠️ Good progress, but improvements are needed.")
    else:
        st.error("❌ You failed to meet sustainability goals.")
