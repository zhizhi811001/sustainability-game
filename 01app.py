import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 🎮 Game Configuration
# ------------------------------

st.title("🌱 Sustainable Industry Simulation Game")

st.sidebar.header("Game Settings")
years = st.sidebar.slider("Select Simulation Years", min_value=5, max_value=10, value=5)

# Sustainability initiatives
initiatives = {
    "Solar Panels": {"CO2 Reduction": 10, "Cost": 2, "Implementation Years": 2},
    "Heat Recovery System": {"CO2 Reduction": 7, "Cost": 1.5, "Implementation Years": 3},
    "Green Hydrogen": {"CO2 Reduction": 20, "Cost": 5, "Implementation Years": 4},
    "Recycled Materials": {"CO2 Reduction": 8, "Cost": 1, "Implementation Years": 1},
    "Electrify Logistics Fleet": {"CO2 Reduction": 12, "Cost": 3, "Implementation Years": 2},
    "IoT Energy Monitoring": {"CO2 Reduction": 5, "Cost": 1, "Implementation Years": 1},
    "Staff Green Training": {"CO2 Reduction": 3, "Cost": 0.5, "Implementation Years": 1},
}

# Initial settings
starting_co2 = 100  # Initial CO2 level (percentage of baseline)
co2_reduction_target = 50  # Target CO2 reduction percentage
budget = 10  # Initial budget in $M

# Store game progress
game_data = {
    "Year": [],
    "Chosen Initiatives": [],
    "CO2 Reduction": [],
    "Total Cost": [],
    "Remaining Budget": [],
    "Remaining_CO2": [],
}

# ------------------------------
# 🏁 Game Loop
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

            budget -= total_cost
            starting_co2 -= total_co2_reduction  # Reduce emissions

            # Store data
            game_data["Year"].append(year)
            game_data["Chosen Initiatives"].append(selected_initiatives)
            game_data["CO2 Reduction"].append(total_co2_reduction)
            game_data["Total Cost"].append(round(total_cost, 2))
            game_data["Remaining Budget"].append(round(budget, 2))
            game_data["Remaining_CO2"].append(round(starting_co2, 2))

            st.success(f"Year {year} decisions saved! See results below.")

    st.write("---")

# ------------------------------
# 📊 Results & Visualization
# ------------------------------

if len(game_data["Year"]) > 0:
    df_results = pd.DataFrame(game_data)

    st.header("📊 Game Summary")
    st.write(df_results)

    # Fix CO2 reduction tracking and plot the corrected chart
    st.subheader("📉 CO2 Emission Reduction Over Time")
fig, ax = plt.subplots(figsize=(8, 5))

# Fix year formatting
df_results["Year"] = df_results["Year"].astype(int)

# Fix CO2 calculation
df_results["Remaining_CO2"] = starting_co2 - df_results["CO2 Reduction"].cumsum()

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
   if starting_co2 <= 100 - co2_reduction_target:
    st.success("🎉 Congratulations! You have met the sustainability goal! 🎉")
elif budget <= 0:
    st.error("⚠️ Budget depleted! Try optimizing your strategy next time.")
