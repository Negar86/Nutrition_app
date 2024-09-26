import streamlit as st

import numpy as np 
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from pyecharts.charts import Bar
from pyecharts import options as opts
import matplotlib.cm as cm 
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="NutriBite",page_icon=":bowl_with_spoon:",layout="wide")
st.sidebar.image('./pic/logo.png')

# define dataset
df = pd.read_csv("./DB/after_cleaning.csv")

# Title 
st.subheader('Food Calories Tracker')
# Initialize session state for the basket
if 'basket' not in st.session_state:
    st.session_state.basket = []

# Create columns for select boxes and input field
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# Add an "All" option to the food groups
food_groups = df['FoodGroup'].unique().tolist()
food_groups.insert(0, "All")

with col1:
    # User selects a food group
    selected_group = st.selectbox("Food group:",  ["All"] + sorted(df['FoodGroup'].unique()))

# Filter the dataframe based on the selected FoodGroup
if selected_group == 'All':
    filtered_df = df
else:
    filtered_df = df[df['FoodGroup'] == selected_group]

with col2:
    # remove duplicate names from list
    unique_foods = sorted(filtered_df['FoodName'].unique())

    # User selects a food item from the unique food names list
    selected_food = st.selectbox("Food:", unique_foods)
            
 
with col3:
    # Filter the dataframe to show only the rows for the selected food
    food_filtered_df = filtered_df[filtered_df['FoodName'] == selected_food]

    # User selects a type of food from the filtered list
    selected_desc = st.selectbox("Desc:", food_filtered_df['Desc'].unique())  # Use .unique() to remove duplicates


with col4:
    # User inputs the amount in grams
    amount_in_grams = st.number_input("Amount (grams)", min_value=1, value=100, step=1)

with col5:

    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    # Add button to add the selected food and amount to the basket
    if st.button('Add'):
        item_details = df[(df['FoodName'] == selected_food) & (df['Desc'] == selected_desc)].iloc[0].to_dict()
        #item_details = df[(df['FoodName'] == selected_food) ].iloc[0].to_dict()
        item_details['Amount_grams'] = amount_in_grams
        item_details['Total_Energy_kcal'] = (amount_in_grams / 100) * item_details['Energy_kcal']
                

        st.session_state.basket.append(item_details)
        #st.success(f"Added {amount_in_grams} grams of {selected_food} .")


    # Display the basket contents
st.write("**Today Food consumption:**")
if st.session_state.basket:
    total_energy = 0
    for item in st.session_state.basket:
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1,1])
        with col1:
            st.write(f"{item['FoodName']}")
                
        with col2:
            st.write(f"{item['Desc']}")

        with col3:
            st.write(f" {item['Amount_grams']} gr")

        with col4:
            st.write(f" {round(item['Total_Energy_kcal'],2)} kcal")
                
        with col5:
            if st.button(f"Remove", key=f"remove_{item['FoodName']}"):
                st.session_state.basket = [i for i in st.session_state.basket if i['Desc'] != item['Desc']]
                st.experimental_rerun()
        total_energy += item['Total_Energy_kcal']



# Finish button to calculate total calories
if st.button("Finish"):
    total_calories = sum(item['Total_Energy_kcal'] for item in st.session_state.basket)
    st.write(f"Total calories for today: **{round(total_calories,2)}** kcal")
            
    col1, col2 = st.columns(2)
    with col1:
        # Show donut plot for Macros
        macro_totals = {'Protein_g': 0, 'Fat_g': 0, 'Carb_g':0}

        # Sum up the macronutrients for all items in the basket
        if 'basket' in st.session_state and st.session_state.basket:
            for item in st.session_state.basket:
                for macro in macro_totals.keys():
                    macro_totals[macro] += item.get(macro, 0)*(amount_in_grams/100)
                    #item_details['Total_Protein_g'] = (amount_in_grams / 100) * item_details['Protein_g']

        # Create the donut chart
        labels = list(macro_totals.keys())
        values = list(macro_totals.values())
        colors = ['#be29ec', '#fffb05', '#32CD32', '#ff48a5','#a87e62'] 
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=colors))])
        fig.update_traces(hoverinfo= 'percent',textinfo='percent', showlegend=True)
        fig.update_layout(title_text="Macros")

        # Display the donut chart in Streamlit
        st.plotly_chart(fig)
            


    with col2:
        # Show table for Micros
        macro_totals = {'Energy_kcal' : 0, 'Protein_g': 0, 'Fat_g': 0, 'Carb_g': 0, 'Sugar_g':0, 'Fiber_g':0}

        # Sum up the macronutrients for all items in the basket
        if 'basket' in st.session_state and st.session_state.basket:
            for item in st.session_state.basket:
                for macro in macro_totals.keys():
                    macro_totals[macro] += round(item.get(macro, 0)*(amount_in_grams/100),4)

        # Convert the dictionary to a sorted list of tuples (descending by values)
        sorted_macro_totals = sorted(macro_totals.items(), key=lambda x: x[1], reverse=True)

        # Extract the sorted labels and values
        labels = [item[0] for item in sorted_macro_totals]
        values = [item[1] for item in sorted_macro_totals]

                

        # Format the values to 4 decimal places for display on the bars
        formatted_values = [f"{value:.4f}" for value in values] 

        # Create the table
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Macros', 'Amount'],
                        fill_color='paleturquoise',
                        align='center'),
            cells=dict(values=[labels, formatted_values],  # First column is 'labels', second column is 'values'
                    fill_color='lavender',
                    align='center'))
                ])
        
                
        # Display the bar chart in Streamlit
        st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
         # Show barchat for vitamins
        vitamin_total = {'VitA_mg' : 0,'Thiamin_mg':0,'Riboflavin_mg':0,'Niacin_mg':0 ,'VitB6_mg': 0,'Folate_mg':0 ,'VitB12_mg': 0, 'VitC_mg': 0, 'VitE_mg': 0}
        # Sum up the macronutrients for all items in the basket
        if 'basket' in st.session_state and st.session_state.basket:
            for item in st.session_state.basket:
                for vitamin in vitamin_total.keys():
                    vitamin_total[vitamin] += round(item.get(vitamin, 0)*(amount_in_grams/100),4)

        # Convert the dictionary to a sorted list of tuples (descending by values)
        sorted_vitamin_total = sorted(vitamin_total.items(), key=lambda x: x[1], reverse=True)

        # Extract the sorted labels and values
        labels = [item[0] for item in sorted_vitamin_total]
        values = [item[1] for item in sorted_vitamin_total]

        # Assign different colors for each bar
        colors = ['#ff7400', '#ff8d00', '#ffa700', '#ffce00', '#ffde1a', 
                        '#ffc284', '#ffd28e', '#ffe096', '#ffee8b']

        # Format the values to 3 decimal places for display on the bars
        formatted_values = [f"{value:.4f}" for value in values] 

        # Create the horizontal bar chart
        fig = go.Figure(data=[go.Bar(x=values, y=labels, orientation='h', marker_color=colors,text=formatted_values,textposition='outside',insidetextanchor='start')])

        # Update the layout to show the title and axis labels
        fig.update_layout(
            title_text="Vitamins (mg)",
            #xaxis_title=" Amount (mg)",
            #yaxis_title="Micro-nutrient",
            yaxis=dict(categoryorder='total ascending')
                )

        # Display the bar chart in Streamlit
        st.plotly_chart(fig)
            

    with col2:
        # Show barchat for mineral
        mineral_total = {'Calcium_mg':0, 'Iron_mg':0,'Magnesium_mg':0,'Manganese_mg':0,'Phosphorus_mg':0,'Zinc_mg':0, 'Copper_mg':0, 'Selenium_mg':0}

        # Sum up the macronutrients for all items in the basket
        if 'basket' in st.session_state and st.session_state.basket:
            for item in st.session_state.basket:
                for mineral in mineral_total.keys():
                    mineral_total[mineral] += round(item.get(mineral, 0)*(amount_in_grams/100),4)

        # Convert the dictionary to a sorted list of tuples (descending by values)
        sorted_mineral_total = sorted(mineral_total.items(), key=lambda x: x[1], reverse=True)

        # Extract the sorted labels and values
        labels = [item[0] for item in sorted_mineral_total]
        values = [item[1] for item in sorted_mineral_total]

        # Assign different colors for each bar
        colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0', 
                        '#92d2f9', '#a8daf9', '#bbdcf0', '#e4edf2']

        # Format the values to 3 decimal places for display on the bars
        formatted_values = [f"{value:.4f}" for value in values] 

        # Create the horizontal bar chart
        fig = go.Figure(data=[go.Bar(x=values, y=labels, orientation='h', marker_color=colors,text=formatted_values,textposition='outside',insidetextanchor='start')])

        # Update the layout to show the title and axis labels
        fig.update_layout(
            title_text="Minerals (mg)",
            #xaxis_title=" Amount (mg)",
            #yaxis_title="Micro-nutrient",
            yaxis=dict(categoryorder='total ascending')
                )


        # Display the bar chart in Streamlit
        st.plotly_chart(fig)


        # Reset basket after calculation
        st.session_state.basket = []  
