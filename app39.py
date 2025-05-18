import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Engineered Landfill Design & Analysis", layout="wide")
st.title("🗑️ Engineered Landfill Analysis and Design Dashboard")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
waste_depth = st.sidebar.slider("Waste Depth (m)", 5, 60, 20)
liner_thickness = st.sidebar.slider("Liner Thickness (m)", 0.1, 2.0, 0.5)
slope_angle = st.sidebar.slider("Slope Angle (degrees)", 10, 60, 30)
permeability = st.sidebar.number_input("Waste Permeability (m/day)", 0.00001, 1.0, 0.001, format="%f")
rainfall = st.sidebar.slider("Average Daily Rainfall (mm/day)", 0, 100, 10)
area = st.sidebar.number_input("Landfill Area (m^2)", 1000, 100000, 10000)
unit_weight = st.sidebar.slider("Waste Unit Weight (kN/m³)", 5, 25, 12)
cohesion = st.sidebar.slider("Waste Cohesion (kPa)", 0, 50, 5)
friction_angle = st.sidebar.slider("Friction Angle (°)", 10, 45, 30)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["2D Landfill View", "Settlement Analysis", "Leachate Generation", "Slope Stability"])

with tab1:
    st.subheader("📐 Schematic View of Landfill")
    fig, ax = plt.subplots()
    base_length = waste_depth / np.tan(np.radians(slope_angle))
    ax.plot([0, base_length, 0], [0, waste_depth, waste_depth], color='brown', linewidth=3)
    ax.fill([0, base_length, 0], [0, waste_depth, waste_depth], color='sandybrown', alpha=0.7)
    ax.set_title("Simplified Landfill Cross-Section")
    ax.set_xlabel("Base Width (m)")
    ax.set_ylabel("Height (m)")
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.subheader("📉 Settlement Analysis")
    settlement_coefficient = 0.02  # m/kN/m²
    applied_stress = unit_weight * waste_depth  # kPa
    settlement = settlement_coefficient * applied_stress
    st.metric("Estimated Settlement (m)", round(settlement, 2))
    st.progress(min(settlement / 5, 1.0))

with tab3:
    st.subheader("💧 Leachate Generation & Flow")
    rainfall_m = rainfall / 1000  # mm to m
    leachate_volume = rainfall_m * area  # m³/day
    leachate_percolation = leachate_volume * permeability  # flow component
    st.metric("Leachate Volume (m³/day)", round(leachate_volume, 2))
    st.metric("Leachate Flow (m³/day)", round(leachate_percolation, 5))

    fig2, ax2 = plt.subplots()
    days = np.arange(0, 30)
    flow = leachate_percolation * np.exp(-0.05 * days)
    ax2.plot(days, flow, label='Leachate Flow', color='blue')
    ax2.set_title("Leachate Flow Over Time")
    ax2.set_xlabel("Days")
    ax2.set_ylabel("Flow (m³/day)")
    ax2.grid(True)
    st.pyplot(fig2)

with tab4:
    st.subheader("🧱 Slope Stability Analysis")
    FOS = (cohesion + unit_weight * waste_depth * np.tan(np.radians(friction_angle))) / (unit_weight * waste_depth * np.sin(np.radians(slope_angle)))
    st.metric("Factor of Safety (FOS)", round(FOS, 2))

    fig3, ax3 = plt.subplots()
    stability_colors = ['red' if FOS < 1 else 'orange' if FOS < 1.5 else 'green']
    ax3.bar(['FOS'], [FOS], color=stability_colors)
    ax3.axhline(y=1.5, color='black', linestyle='--', label='Min Safe FOS')
    ax3.set_ylim(0, max(2, FOS + 0.5))
    ax3.set_title("Slope Stability Factor of Safety")
    ax3.legend()
    st.pyplot(fig3)

# Footer
st.markdown("---")
st.caption("Developed by Rohit Maurya, Hindustan College of Science and Technology")