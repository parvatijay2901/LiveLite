import streamlit as st

def get_input_for_risk_score(mapped_user_inputs):
    risk_predict_input = {'DPQ020': [mapped_user_inputs['internal_mental_health']], 
                        'DPQ050': [mapped_user_inputs['internal_poor_appetite_overeating']], 
                        'PAQ670': [mapped_user_inputs['internal_activity_level']], 
                        'DBQ700': [mapped_user_inputs['internal_diet_condition']], 
                        'HUQ010': [mapped_user_inputs['internal_health_condition']],
                        'RIAGENDR': [mapped_user_inputs['internal_sex']], 
                        'RIDAGEYR': [mapped_user_inputs['internal_age']], 
                        'RIDRETH3': [mapped_user_inputs['internal_ethnicity']], 
                        'SMQ040': [mapped_user_inputs['internal_smoke_cig']],
                        'SLD012': [mapped_user_inputs['internal_sleep_hrs']]
                        }
    return risk_predict_input

def display_risk_score(risk_score):
    if risk_score < 100:
        if risk_score <= 25:
            color = '#add8e6'
        elif risk_score > 25 and risk_score <= 50:
            color = '#add8e6'
        elif risk_score > 50 and risk_score <= 75:
            color = '#ffff99'  
        else:
            color = '#ffa07a' 
        
        risk_score = str(risk_score) + "%"
        
    else:
        risk_score = "Obese"
        color = '#ff6242'
        
    donut_plot = f"""<div style="width: 250px; height: 250px;">
    <svg width="250" height="250" viewBox="0 0 250 250">
    <!-- Outer circle (ring) -->
    <circle cx="125" cy="125" r="100" fill="none" stroke={color} stroke-width="50" />
    <!-- Inner circle (center) -->
    <circle cx="125" cy="125" r="50" fill="none" />
    <!-- Text showing the risk score -->
    <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="30" font-weight="bold" fill="white">{risk_score}</text>
    </svg>
    </div>
    """
    st.markdown(donut_plot, unsafe_allow_html=True)
    return donut_plot

def display_risk_suggestion(risk_score):
    if risk_score <= 25:
        text = f"""Based on your assessment, your risk of obesity 
        is currently low at {risk_score}%. To maintain this healthy level, why not explore
        our tips for delicious and nutritious meals, and discover fun ways to stay active?"""
    elif risk_score > 25 and risk_score <= 50:
        text = f"""Your current risk of obesity is moderate at {risk_score}%. This is a good 
        opportunity to explore ways to optimize your health further. We have some helpful resources
        for balanced eating and enjoyable physical activities that can make a positive difference."""
    elif risk_score > 50 and risk_score <= 75:
        text = f"""Based on your assessment, your risk of obesity is currently high at {risk_score}%. 
        This may be a good time to consider some lifestyle changes. We have a collection of personalized 
        recommendations for healthy eating and physical activity that can help you reach your goals."""
    elif risk_score > 75 and risk_score <= 99:
        text = f"""Your risk of obesity is currently very high at {risk_score}%. It's important to take 
        steps to address this for your overall well-being. We understand this can be challenging, but we're 
        here to support you with personalized guidance on healthy eating and physical activity. 
        Let's work together to achieve your health goals."""
    else:
        text = f"""Based on your assessment, you are Obese. It's important to remember that everyone's journey 
        towards better health is unique, and taking small steps can make a big difference. We understand this can be daunting, 
        but we're here to support you with personalized guidance on healthy eating and physical activity. 
        Let's work together to achieve your health goals."""

    text = f"<center>{text}</center>"
    st.markdown(text, unsafe_allow_html=True)