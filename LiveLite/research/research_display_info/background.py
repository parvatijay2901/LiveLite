import streamlit as st

def display_background():
    st.markdown("""Obesity is ever-growing issue in the modern world. Defined as 'weight that is considered higher than 
                what is considered healthy for a given height' by the CDC. Body Mass Index (BMI) is a general method of 
                defining obesity. BMI in the ranges of 25 to 29.9 kg/m<sup>2</sup> are considered overweight and BMI greater than 
                or equal to 30 kg/m<sup>2</sup> are considered obese. Obesity is nowadays described as a chronic disease that is only 
                increasing in prevalence in all ages and currently now considered to be an ongoing global epidemic of obesity.""", 
                unsafe_allow_html=True)
    st.markdown("""Using the NHANES data collected between the years of 1999 to 2018, we can observe that the prevalence of 
                obesity in the United States has progressively increased from 30.5 to 42.4 %.""",
                unsafe_allow_html=True)