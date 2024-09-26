import streamlit as st
st.set_page_config(page_title="NutriBite",page_icon=":bowl_with_spoon:",layout="wide")
st.sidebar.image('./pic/logo.png')


col1, col2 = st.columns(2)
with col1:
    st.markdown('''
            <p align="left">
                <small style="font-size:20px;">Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) Calculator</small>
            </p>
            ''', unsafe_allow_html=True)

with col2:
    st.image('./pic/body-mass-index.jpg',width=180)

st.markdown('''
            <p align="left">
                <small style="font-size:16px;">Please type requested information</small>
            </p>
            ''', unsafe_allow_html=True)

def calculate_bmi(weight, height):
    bmi = weight / ((height/100)**2)
    return bmi
        

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Normal weight"
    elif 25.0 <= bmi < 30.0:
        return "Pre-obesity"
    elif 30.0 <= bmi < 35.0:
        return "Obesity class I"
    elif 35.0 <= bmi < 40.0:
        return "Obesity class II"
    else:
        return "Obesity class III"

def calculate_target_weight_range(height):
    height_m = height / 100  # Convert height to meters
    # The BMI range for "Normal weight" is 18.5 - 25
    min_normal_weight = 18.5 * (height_m ** 2)
    max_normal_weight = 25 * (height_m ** 2)
    return min_normal_weight, max_normal_weight

def calculate_weight_adjustment(weight, height):
    min_normal_weight, max_normal_weight = calculate_target_weight_range(height)
            
    if weight < min_normal_weight:
        weight_to_gain = min_normal_weight - weight
        return f"You need to gain  {weight_to_gain:.2f} kg to reach the minimum normal weight."
    elif weight > max_normal_weight:
        weight_to_lose = weight - max_normal_weight
        return f"You need to lose  {weight_to_lose:.2f} kg to reach the maximum normal weight."
    else:
        return "Your weight is within the normal range."
  

# for calculating BMR I use The Harris–Benedict equations revised by Mifflin and St Jeor
def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'Female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return None
        
def calculate_tdee(bmr, activity_level):
    activity_factors = {
                        'Sedentary (little or no exercise)': 1.2,
                        'Lightly active (light exercise or sports 1-3 days a week)': 1.375,
                        'Moderately active (moderate exercise or sports 3-5 days a week)': 1.55,
                        'Very active (hard exercise or sports 6-7 days a week)': 1.725,
                        'Extra active (very hard exercise/sports 6 to 7 days per week and physical job)': 1.9}
    return round(bmr * activity_factors.get(activity_level), 2)



# Streamlit application
# Custom CSS to control the size of number input
st.markdown("""
    <style>
    .stNumberInput input {
        width: 5000px; /* Adjust the width as per your requirement */
    }
    </style>
    """, unsafe_allow_html=True)

        
weight = st.number_input("Enter your weight in kilograms:", value=None, placeholder="Type a number")
height = st.number_input("Enter your height in centimeters:", value=None, placeholder="Type a number")
age = st.number_input("Enter your age in years:", value=None, placeholder="Type a number")
gender = st.selectbox("Enter your gender:", ["Female","Male",])
activity_level = st.selectbox('Select your activity level:', 
                                       ['Sedentary (little or no exercise)', 
                                       'Lightly active (light exercise or sports 1-3 days a week)', 
                                       'Moderately active (moderate exercise or sports 3-5 days a week)',
                                       'Very active (hard exercise or sports 6-7 days a week)', 
                                       'Extra active (very hard exercise/sports 6 to 7 days per week and physical job)'])

if st.button('Calculate'):
    bmi = round(calculate_bmi(weight, height),2)
    bmr = round(calculate_bmr(weight, height, age, gender), 2)
    bmi_classification = classify_bmi(bmi)
    tdee = calculate_tdee(bmr, activity_level)
    adjustment_message = calculate_weight_adjustment(weight, height)
    

    if bmi is not None:
        st.write(f"BMI : **{bmi} - {bmi_classification}**")
        st.write(adjustment_message)

        st.write(f"TDEE : **{tdee} kcal/day**")
        st.write(f"Energy to maintain your current weight.")

