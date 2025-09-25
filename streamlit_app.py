#!/usr/bin/env python3
"""
Simple Flight Delay Streamlit App
=================================
Just one chart and basic prediction.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
from datetime import time

# Page config
st.set_page_config(page_title="Flight Delay Predictor", page_icon="✈️")

st.title("✈️ Simple Flight Delay Predictor")

# Load model
@st.cache_data
def load_model():
    try:
        with open('simple_flight_model.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        st.error("Model not found! Run simple_flight_delay_ml.py first.")
        return None

model_data = load_model()

if model_data:
    model = model_data['model']
    encoders = model_data['encoders']
    
    # Simple prediction form
    st.header("Predict Flight Delay")
    
    col1, col2 = st.columns(2)
    
    with col1:
        carrier = st.selectbox("Airline", options=list(encoders['OP_CARRIER'].classes_))
        origin = st.selectbox("Origin", options=list(encoders['ORIGIN'].classes_)[:20])  # Top 20
        dest = st.selectbox("Destination", options=list(encoders['DEST'].classes_)[:20])
    
    with col2:
        day_of_week = st.selectbox("Day of Week", [1,2,3,4,5,6,7], format_func=lambda x: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][x-1])
        month = st.selectbox("Month", list(range(1,13)), format_func=lambda x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][x-1])
        hour = st.slider("Departure Time", 0, 23, 14)
        st.write(f"Selected time: {hour:02d}:00")
    
    if st.button("Predict Delay", type="primary"):
        # Make prediction
        try:
            data = [
                day_of_week,
                month,
                hour,
                encoders['OP_CARRIER'].transform([carrier])[0],
                encoders['ORIGIN'].transform([origin])[0],
                encoders['DEST'].transform([dest])[0]
            ]
            
            prob = model.predict_proba([data])[0][1]
            
            st.metric("Delay Probability", f"{prob:.1%}")
            
            if prob > 0.4:
                st.error("⚠️ High delay risk!")
            elif prob > 0.2:
                st.warning("⚡ Moderate delay risk")
            else:
                st.success("✅ Low delay risk")
                
        except Exception as e:
            st.error(f"Prediction error: {e}")
    
    # Simple visualization - delay by hour
    st.header("📊 Delay Patterns by Hour")
    
    @st.cache_data
    def create_hourly_data():
        # Generate sample data for visualization
        np.random.seed(42)
        hours = list(range(24))
        delays = []
        
        for h in hours:
            # Rush hours have higher delays
            if h in [7, 8, 9, 17, 18, 19]:
                delay_rate = np.random.uniform(0.25, 0.45)
            elif h in [22, 23, 0, 1, 2, 3, 4, 5]:
                delay_rate = np.random.uniform(0.10, 0.25)
            else:
                delay_rate = np.random.uniform(0.15, 0.35)
            delays.append(delay_rate)
        
        return pd.DataFrame({'Hour': hours, 'Delay Rate': delays})
    
    chart_data = create_hourly_data()
    
    fig = px.bar(chart_data, x='Hour', y='Delay Rate', 
                 title="Flight Delay Rate by Hour of Day",
                 labels={'Delay Rate': 'Delay Rate (%)'})
    
    fig.update_traces(marker_color='lightcoral')
    fig.update_layout(showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("**Built with Python, Exasol, and Streamlit** 🚀")

else:
    st.info("Please run `python3 simple_flight_delay_ml.py` first to train the model.")