import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 🎮 Game Introduction
# ------------------------------

st.title("🏭 Sustainable Industry Simulation Game: Industry 4.0 & Green Supply Chains")

st.markdown("""
## 📌 Scenario Title: Achieving Sustainable Supply Chain Excellence through Green Servitisation Innovation
### 🎯 Goal:
Transform a traditional manufacturing company into a **Green Servitisation-Oriented Business Model (GS-OBM)** by integrating **Industry 4.0 technologies**, **ESG compliance**, and **Green Sustainable Supply Chain Management (GSSCM)** over a **5-year period**.

---

### 🏭 **Background Story**
You are the **Sustainability Director** of **EcoMotive Industries**, a leading manufacturing company that produces **automotive parts**. Due to increasing regulatory and customer demands for **sustainable production**, your company must transition from a **traditional product-based model** to a **servitisation-based business model** that focuses on **circular economy principles** and **green supply chain innovation**.

### 🚀 **Key Challenges**
1. **Government Regulations & ESG Compliance**: New laws require all manufacturing firms to **reduce CO₂ emissions by 30% within 5 years**.
2. **Industry 4.0 Technological Adoption**: The company must adopt **smart manufacturing, digital twins, IoT-based monitoring, and AI-driven logistics**.
3. **Sustainable Supply Chain Management**: You must **reduce waste, improve resource efficiency, and enhance reverse logistics**.
4. **Financial Constraints**: You have a **$15M budget** to make strategic investments while ensuring profitability.

---

## 📅 Yearly Decision Process
Each year, you must choose **up to 3 sustainability initiatives** to invest in.
Each initiative has **different costs, implementation time, and CO₂ impact**.

| **Initiative** | **Impact** | **Cost** | **Implementation Time** |
|--------------|-----------|----------|----------------|
| **IoT-Enabled Smart Manufacturing** 🏭📡 | -12% CO₂ emissions | $3M | 3 years |
| **AI-Optimized Logistics Routes** 🚚🤖 | -10% CO₂ emissions | $2M | 2 years |
| **Fleet Electrification** ⚡🚛 | -15% CO₂ emissions | $5M | 4 years |
| **Public Awareness & Green Branding** 📢 | -5% CO₂ emissions | $1M | 1 year |
| **Green Procurement (Sustainable Suppliers)** 🌱 | -8% CO₂ emissions | $2M | 2 years |
| **Automated Sorting & Recycling System** 🔄 | -15% CO₂ emissions | $4M | 3 years |
| **Reverse Logistics for Parts Recovery** ♻️ | -10% CO₂ emissions | $2.5M | 3 years |
| **Hydrogen-Powered Equipment** 🔋 | -20% CO₂ emissions | $6M | 5 years |

### 📌 Notes:
- **IoT Smart Manufacturing** improves **real-time efficiency monitoring**.
- **AI-Optimized Logistics** helps in **predictive supply chain decision-making**.
- **Fleet Electrification & Hydrogen Power** have **high impact but high cost**.
- **Reverse Logistics** promotes **circular economy principles**.
- **Green Procurement** ensures **supply chain sustainability**.

---
""")

st.sidebar.header("Game Settings")
years = st.sidebar.slider("Select Simulation Years", min_value=3, max_value=7, value=5)


# ------------------------------
# 🎮 Game Configuration
# ------------------------------

st.title("🏭 Sustainable Industry Simulation Game: Industry 4.0 & Green Supply Chains")

st.sidebar.header("Game Settings")
years = st.sidebar.slider("Select Simulation Years", min_value=3, max_value=7, value=5)

# Sustainability initiatives based on Servitisation & Green Supply Chain Management
initiatives = {
    "IoT-Enabled Smart Manufacturing": {"CO2 Reduction": 12, "Cost": 3, "Implementation Years": 3},
    "AI-Optimized Logistics Routes": {"CO2 Reduction": 10, "Cost": 2, "Implementation Years": 2},
    "Fleet Electrification": {"CO2 Reduction": 15, "Cost": 5, "Implementation Years": 4},
    "Public Awareness & Green Branding": {"CO2 Reduction": 5, "Cost": 1, "Implementation Years": 1},
    "Green Procurement (Sustainable Suppliers)": {"CO2 Reduction": 8, "Cost": 2, "Implementation Years": 2},
    "Automated Sorting & Recycling System": {"CO2 Reduction": 15, "Cost": 4, "Implementation Years": 3},
    "Reverse Logistics for Parts Recovery": {"CO2 Reduction": 10, "Cost": 2.5, "Implementation Years": 3},
    "Hydrogen-Powered Equipment": {"CO2 Reduction": 20, "Cost": 6, "Implementation Years": 5},
}

# Initial settings
starting_co2 = 100  # Initial CO2 level (percentage of baseline)
co2_reduction_target = 30  # Target CO2 reduction percentage
total_budget = 15  # Total budget in $M for all years

# Initialize session state
if 'game_data' not in st.session_state:
    st.session_state.game_data = {
        "Year": [],
        "Chosen Initiatives": [],
        "CO2 Reduction": [],
        "Total Cost": [],
        "Remaining Budget": [],
    }
    st.session_state.remaining_budget = total_budget  # Initialize remaining budget

# ------------------------------
# 🏁 Game Loop
# ------------------------------

st.header("📅 Yearly Decision-Making")

for year in range(1, years + 1):
    st.subheader(f"Year {year}")

    # Use a unique key for each multiselect and button to avoid conflicts
    selected_initiatives = st.multiselect(
        f"Select up to 3 initiatives for Year {year}",
        list(initiatives.keys()),
        default=[],
        max_selections=3,
        key=f"initiatives_{year}",  # Unique key for each multiselect
    )

    # Use a unique key for each button to avoid conflicts
    if st.button(f"Confirm Choices for Year {year}", key=f"confirm_{year}"):
        if not selected_initiatives:
            st.warning("Please select at least one initiative.")
        else:
            total_co2_reduction = sum(initiatives[c]["CO2 Reduction"] for c in selected_initiatives)
            total_cost = sum(initiatives[c]["Cost"] for c in selected_initiatives)

            if total_cost > st.session_state.remaining_budget:
                st.error("⚠️ Not enough budget to implement these initiatives. Please adjust your choices.")
            else:
                st.session_state.remaining_budget -= total_cost  # Deduct from remaining budget

                # Store data in session state
                st.session_state.game_data["Year"].append(year)
                st.session_state.game_data["Chosen Initiatives"].append(selected_initiatives)
                st.session_state.game_data["CO2 Reduction"].append(total_co2_reduction)
                st.session_state.game_data["Total Cost"].append(round(total_cost, 2))
                st.session_state.game_data["Remaining Budget"].append(round(st.session_state.remaining_budget, 2))

                st.success(f"Year {year} decisions saved! See results below.")

    st.write("---")

# ------------------------------
# 📊 Results & Visualization
# ------------------------------

if len(st.session_state.game_data["Year"]) > 0:
    df_results = pd.DataFrame(st.session_state.game_data)

    # Ensure cumulative CO2 reduction is tracked correctly
    df_results["Cumulative_CO2_Reduction"] = df_results["CO2 Reduction"].cumsum()
    df_results["Remaining_CO2"] = starting_co2 - df_results["Cumulative_CO2_Reduction"]

    st.header("📊 Game Summary")
    st.write(df_results)

    # Fix CO2 reduction tracking and plot the corrected chart
    st.subheader("📉 CO2 Emission Reduction Over Time")
    
    fig, ax = plt.subplots(figsize=(8, 5))

    # Fix year formatting
    df_results["Year"] = df_results["Year"].astype(int)

    # Ensure CO2 levels decrease each year
    ax.plot(
        df_results["Year"],
        df_results["Remaining_CO2"],
        marker="o",
        linestyle="-",
        label="CO2 Reduction Progress",
    )

    # Draw the target reduction line
    ax.axhline(y=starting_co2 - co2_reduction_target, color="r", linestyle="--", label="Target Reduction")

    ax.set_xlabel("Year")
    ax.set_ylabel("CO2 Emissions (% of baseline)")
    ax.set_title("CO2 Emission Reduction Over Time")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # Display Final Result
    if df_results["Remaining_CO2"].iloc[-1] <= starting_co2 - co2_reduction_target:
        st.success("🎉 Congratulations! You have optimized the supply chain for sustainability! 🎉")
    elif st.session_state.remaining_budget <= 0:
        st.error("⚠️ Budget depleted! Try optimizing your strategy next time.")