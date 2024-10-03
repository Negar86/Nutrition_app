import streamlit as st

import numpy as np 
import pandas as pd

st.set_page_config(page_title="NutriBite",page_icon=":bowl_with_spoon:",layout="wide")
st.sidebar.image('./pic/logo.png')

df = pd.read_csv('./DB/cluster.csv')

st.header("Alternative Choices")

st.write("Select a food to find similar foods based on their nutritional profile.")
selected_food = st.selectbox("Choose a food item:", df['FoodName'].unique())




# Get the corresponding Food Group and Cluster for the selected description
selected_row = df[df['FoodName'] == selected_food].iloc[0]
selected_food_group = selected_row['FoodGroup']
selected_cluster = selected_row['Cluster']

# Filter the DataFrame for the same Food Group and Cluster
filtered_df = df[(df['Cluster'] == selected_cluster)&(df['Energy_kcal']<= selected_row['Energy_kcal'])&(df['FoodGroup']== selected_row['FoodGroup'])]

# Sort by Energy_kcal and show top 10
top_30 = filtered_df.sort_values(by='Energy_kcal', ascending=False).head(30)
final = top_30[['FoodName','Desc','Energy_kcal','Protein_g', 'Fat_g', 'Carb_g', 'Sugar_g', 'Fiber_g']].reset_index()

st.markdown(
    f'<div style="background-color: lightgreen; padding: 10px; border-radius: 5px; color: black;">'
    f'<strong>Alternative for {selected_food} : {selected_food_group} Group  </strong>'
    '</div>',
    unsafe_allow_html=True
)


# Display the results
st.dataframe(final)