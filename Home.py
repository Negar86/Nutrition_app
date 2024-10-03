import streamlit as st

# Page config
st.set_page_config(page_title="NutriBite",page_icon=":bowl_with_spoon:",layout="wide")
st.sidebar.image('./pic/logo.png')


st.subheader('Overview')
tab1, tab2 = st.tabs(["Welcome", "Guidline"])
with tab1:
    st.markdown('''
            
        <p align="justify">Welcome to NutriBite - Your Personalized Nutrition Companion!</p>
        <p align="justify">We're excited to have you on this journey towards better health, balanced nutrition, and achieving your ideal weight! Whether you're looking to improve your overall well-being, gain healthy weight, or simply maintain a balanced lifestyle, NutriBite is here to help you every step of the way.</p>
        
        <p align="justify">✨ <b>Evaluate Your Current Situation:</b> </p>
        <p align="justify"> Start by understanding where you are with our easy-to-use assessment tools. Analyze your nutrition habits, identify areas for improvement, and get personalized insights tailored just for you.</p>

        <p align="justify">🥗 <b>Plan for Better Nutrition</b></p>
        <p align="justify"> We'll provide you with a customized nutrition plan that fits your goals, whether you're aiming to gain healthy weight, optimize your diet, or enhance your energy levels. Our plans are flexible, easy to follow, and designed to support long-term success.</p>

        <p align="justify">💪 <b>Achieve Your Goals:</b></p>
        <p align="justify">Track your progress, stay motivated with daily tips, and make informed choices that work for your body and lifestyle. We're here to empower you to build lasting habits for a healthier and happier you.</p>
        
        <p align="justify">Let's get started on your journey to better health and nutrition!</p>

        ''', unsafe_allow_html=True)
        
with tab2:
    st.markdown('''
         
            <h3> BMI <em>(Body Mass Index) </em></h3>    
            <h4>Definition</h4>
            <p align="justify">BMI is an estimate of body fat and a good measure of your patients' risk for diseases that can occur with overweight and obesity. For adults, a healthy weight is defined as the appropriate body weight in relation to height. This ratio of weight to height is known as the body mass index (BMI).</p>
            <p align="justify">BMI = kg/m2 </p>
            <h4> Range (WHO)</h4>
            <ul>
                <li> Severely Underweight: <16 kg/m2</li>
                <li> Underweight: 16.0 to 18.4 kg/m2</li>
                <li> Normal weight: 18.5 to 24.9 kg/m2</li>
                <li> Moderately Obese: 30.0 to 34.9 kg/m2</li>
                <li> Overweight: 25.0 to 29.9 kg/m2</li>
                <li> Severely Obese: 35.0 to 39.9 kg/m2</li>
                <li> Morbidly Obese: ≥40.0 kg/m2</li>

            </ul>
            <h4>chart</h4>
            <p align="justify">Body mass index (BMI) chart Contributed from BMI chart.</p>
            <p align="left">
              <img src="https://www.ncbi.nlm.nih.gov/books/NBK535456/bin/640px-Bmi-chart_colored.jpg" width="60%">
            </p>

            ''', unsafe_allow_html=True)
            
    st.markdown("""---""")

    st.markdown('''
            <div>
            <h3 >BMR <em>(Basal Metabolic Rate)</em></h3>
            <p style="text-align:justify"> BMR refers to the number of calories your body burns each day to keep you alive. BMR does not include physical activity, the process of digestion, or things like walking from one room to another.</p>

            <h4>BMR Calculation</h4>
            <ul>
                <li> Women = 655 + (9.6 X weight in kg) + (1.8 x height in cm) – (4.7 x age in yrs)</li>
                <li> Men = 66 + (13.7 X weight in kg) + (5 x height in cm) – (6.8 x age in yrs)</li>
            
            <p style="text-align:justify"></p>
        
            ''', unsafe_allow_html=True)

    st.markdown("""---""")

    st.markdown('''
            <div>
            <h3> TDEE <em>(Total Daily Energy Expenditure)</em></small></h3>

            <h4>Definition</h4>
            <p align="justify">The amount of energy your body requires to run successfully.  TDEE is often used in order to calculate calorie intake for people looking to lose or gain weight.  If you want to lose weight you have to consume less calories than your TDEE, this creates a calorie deficit.  If you want to gain weight you have to consume more calories than your TDEE, this creates calorie surplus.  Obviously if you eat the same amount, you will be in calorie maintenance and your body weight will remain the same.</p>
            <h4>TDEE Calculation</h4>
            <p align="justify">TDEE consists of two factors:</p>
            <ul>
                <li> Basal Metabolic Rate</li>
                <li> Any Additional Energy Burned Through Exercise</li>
            <p align="justify"></p>
            <p align="justify">TDEE = BMR x Activity Level</p>
            <h4>Additional energy you burn daily:</h4>
            <ul>
                <li> Sedentary (little or no exercise) : 1.2 </li>
                <li> Light activity (light exercise/sports 1 to 3 days per week) : 1.375 </li>
                <li> Moderate activity (moderate exercise/sports 3 to 5 days per week) : 1.55 </li>
                <li> Very active (hard exercise/sports 6 to 7 days per week) : 1.725 </li>
                <li> Extra active (very hard exercise/sports 6 to 7 days per week and physical job) : 1.9 </li>
            ''', unsafe_allow_html=True)
