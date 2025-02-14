import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 🎮 Game Introduction
# ------------------------------

st.title("🏭 Kalundborg Eco-Industrial Park Simulation Game")

st.markdown("""
## 🌍 Scenario Title: Industrial Symbiosis at Kalundborg – A Circular Economy Challenge
### 🎯 Goal:
As the **Sustainability Manager** of the **Kalundborg Industrial Park**, optimize **resource sharing, waste reduction, and energy efficiency** while ensuring financial sustainability over **5 years**.

---
### 🏢 **Background Story**
🌱 **The Kalundborg Model**  
Kalundborg, Denmark, is home to **the world’s most renowned industrial symbiosis network**.  
- **Companies collaborate** to use each other's waste, energy, and resources.  
- **Water, steam, and by-products are exchanged** between industries.  
- **CO₂ emissions, waste, and resource consumption are minimized**.  

**Your challenge:** Expand and optimize this symbiosis network while staying **within financial & regulatory constraints**.

### 🚀 **Key Challenges**
1️⃣ **Resource Efficiency & Circular Economy:**  
   - Improve **water recycling, waste heat utilization, and by-product reuse**.  
   - Reduce **CO₂ emissions by 40% over 5 years**.  

2️⃣ **Financial Constraints & Investment Trade-offs:**  
   - Manage an initial **budget of $50M**.  
   - Invest wisely in **infrastructure, partnerships, and efficiency improvements**.  

3️⃣ **Regulatory Compliance & Stakeholder Coordination:**  
   - Ensure alignment with **EU environmental policies**.  
   - Balance the needs of **public and private stakeholders**.  

---
## 📅 Yearly Decision Process
Each year, choose **up to 3 sustainability initiatives**.  
Each decision affects **cost, CO₂ emissions, and industrial symbiosis performance**.

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

    # CO2 Reduction Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_results["Year"], df_results["Remaining_CO2"], marker="o", linestyle="-", label="CO2 Reduction")

    ax.set_xlabel("Year")
    ax.set_ylabel("CO2 Emissions (% of baseline)")
    ax.set_title("CO2 Emission Reduction Over Time")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    st.subheader(f"🏆 **Final Score: {int(df_results['Cumulative_CO2_Reduction'].iloc[-1])}/100**")
