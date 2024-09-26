import streamlit as st


import numpy as np 
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm 


from pyecharts.charts import Bar
from pyecharts import options as opts

import streamlit.components.v1 as components

st.set_page_config(page_title="NutriBite",page_icon=":bowl_with_spoon:",layout="wide")
st.sidebar.image('./pic/logo.png')


# define dataset
df = pd.read_csv("./DB/after_cleaning.csv")

# Title 
st.header("Nutrition Explorer")
st.subheader("Eat it or Leave it?")

# Add an "All" option to the food groups
food_groups = sorted(df['FoodGroup'].unique().tolist())
food_groups.insert(0, "All")

# Choose between food name or food group
tab1, tab2 = st.tabs(["Food", "Group"])
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        # User selects a food group
        selected_group = st.selectbox("Select the food group:", food_groups)
            
    # Filter the food items based on the selected food group
    if selected_group == "All":
        filtered_df = df
    else:
        filtered_df = df[df['FoodGroup'] == selected_group]
            
    with col2:
        # Allow the user to select a food item from the filtered list
        selected_food = st.selectbox("Select a food:", filtered_df['FoodName'].unique())

    with col3: 
        # Filter the dataframe to show only the rows for the selected food
        food_filtered_df = filtered_df[filtered_df['FoodName'] == selected_food]

        # User selects a type of food from the filtered list
        selected_desc = st.selectbox("Desc:", food_filtered_df['Desc'].unique())  # Use .unique() to remove duplicates
    


    # Extract the nutritional information for the selected food item
    food_info = df[df['Desc'] == selected_desc].iloc[0]
    energy_kcal = food_info['Energy_kcal']

    # Display the Energy_kcal
    st.write(f"Energy of 100 g {selected_food} {selected_desc}: **{energy_kcal} kcal**")


    # Create a bar chart for macronutrients
    macronutrients_chart = (
        Bar()
        .add_xaxis(['Protein_g', 'Fat_g', 'Carb_g', 'Sugar_g', 'Fiber_g'])
        .add_yaxis("", [food_info['Protein_g'], food_info['Fat_g'], food_info['Carb_g'], food_info['Sugar_g'], food_info['Fiber_g']],
                    itemstyle_opts=opts.ItemStyleOpts(color="brown") 
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Macro-nutrients for 100 grams: {selected_food}- {selected_desc}"),
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
    )

    # Create a bar chart for vitamins
    vitamins_chart = (
        Bar()
        .add_xaxis(['VitA_mg', 'Thiamin_mg','Riboflavin_mg','Niacin_mg','VitB6_mg','Folate_mg', 'VitB12_mg', 'VitC_mg', 'VitE_mg'])
        .add_yaxis("", [food_info['VitA_mg'], food_info['Thiamin_mg'],food_info['Riboflavin_mg'],food_info['Niacin_mg'],food_info['VitB6_mg'], food_info['Folate_mg'],food_info['VitB12_mg'], food_info['VitC_mg'], food_info['VitE_mg']],
                itemstyle_opts=opts.ItemStyleOpts(color="orange")  
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Vitamins for 100 grams: {selected_food} - {selected_desc}"),
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
    )


    # Create a bar chart for Minerals
    mineral_chart = (
    Bar()
    .add_xaxis(['Calcium_mg', 'Iron_mg','Magnesium_mg','Manganese_mg','Phosphorus_mg','Zinc_mg', 'Copper_mg', 'Selenium_mg'])
    .add_yaxis("", 
               [food_info['Calcium_mg'], food_info['Iron_mg'],food_info['Magnesium_mg'],food_info['Manganese_mg'],food_info['Phosphorus_mg'], food_info['Zinc_mg'],food_info['Copper_mg'], food_info['Selenium_mg']],
               itemstyle_opts=opts.ItemStyleOpts(color="darkblue")  
              )
    .set_global_opts(
        title_opts=opts.TitleOpts(title=f"Mineral for 100 grams: {selected_food} - {selected_desc}"),
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
    )
)
            
    # Render and embed the bar charts in Streamlit
    components.html(macronutrients_chart.render_embed(), width=1000, height=600)
    components.html(vitamins_chart.render_embed(), width=1000, height=600)
    components.html(mineral_chart.render_embed(), width=1000, height=600)




# GROUP EXPLORER
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        selected_group = st.selectbox("Select food group:", ["All"] + sorted(df['FoodGroup'].unique()))

    with col2:
        order = st.selectbox("Order by:", ["Top 10", "Bottom 10"])

    # Filter the food items based on the selected food group
    if selected_group == "All":
        filtered_df = df
    else:
        filtered_df = df[df['FoodGroup'] == selected_group]


    # Sort the DataFrame by PROTEIN in the selected order
    if order == "Top 10":
        sorted_df = filtered_df.sort_values(by='Protein_g', ascending=False).head(10)
    else:
        sorted_df = filtered_df.sort_values(by='Protein_g', ascending=True).head(10)

    # Plotting the bar chart
    st.subheader(f"Protein-{order}  Foods (100 g) ")

    # Generate a range of colors from the plasma colormap
   # num_bars = len(sorted_df)
    #colors = cm.cividis(np.linspace(0, 1, num_bars))

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(sorted_df['Desc'], sorted_df['Protein_g'], color='purple')
    ax.set_xlabel('Protein (g)')
    ax.invert_yaxis()  # To display the highest at the top

    # Annotating the bars with protein amounts inside the bars
    for bar, desc in zip(bars, sorted_df['FoodName']):
    # Annotating the carb amount
        ax.text(
            bar.get_width() - 0.05,  # Position text slightly to the left of the bar's end
            bar.get_y() + bar.get_height() / 2,  # Center the text vertically on the bar
            f'{bar.get_width():.2f}',  # Format the text (carb amount)
            va='center',  # Vertical alignment
            ha='right',  # Horizontal alignment to keep it inside the bar
            color='white',  # Text color (adjust for contrast)
            fontsize=10,  # Font size (optional)
            weight='bold'  # Make the text bold (optional)
        )
        
        # Annotating the description
        ax.text(
            0.05,  # Position text slightly inside the bar's start
            bar.get_y() + bar.get_height() / 2,  # Center the text vertically on the bar
            desc,  # Add the description text from the DataFrame
            va='center',  # Vertical alignment
            ha='left',  # Horizontal alignment to keep it inside the bar
            color='white',  # Text color (adjust for contrast)
            fontsize=10,  # Font size (optional)
            weight='bold'  # Make the text bold (optional)
        )
    st.pyplot(fig)


    # Sort the DataFrame by CARBO in the selected order
    if order == "Top 10":
        sorted_df = filtered_df.sort_values(by='Carb_g', ascending=False).head(10)
    else:
        sorted_df = filtered_df.sort_values(by='Carb_g', ascending=True).head(10)

    
    st.subheader(f"Carbo - {order}  Foods (100 g) ")
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(sorted_df['Desc'], sorted_df['Carb_g'], color='green')
    ax.set_xlabel('Carbo (g)')
    ax.invert_yaxis()  # To display the highest at the top

    
    for bar, desc in zip(bars, sorted_df['FoodName']):
        ax.text(
            bar.get_width() - 0.05,  # Position text slightly to the left of the bar's end
            bar.get_y() + bar.get_height() / 2,  # Center the text vertically on the bar
            f'{bar.get_width():.2f}',  # Format the text (carb amount)
            va='center',  # Vertical alignment
            ha='right',  # Horizontal alignment to keep it inside the bar
            color='white',  # Text color (adjust for contrast)
            fontsize=10,  # Font size (optional)
            weight='bold'  # Make the text bold (optional)
        )
        
        ax.text(
            0.05,  
            bar.get_y() + bar.get_height() / 2,  
            desc,  
            va='center',  
            ha='left',  
            color='white',  
            fontsize=10,  
            weight='bold'  
        )
    st.pyplot(fig)


    
    # Sort the DataFrame by FAT in the selected order
    if order == "Top 10":
        sorted_df = filtered_df.sort_values(by='Fat_g', ascending=False).head(10)
    else:
        sorted_df = filtered_df.sort_values(by='Fat_g', ascending=True).head(10)

    st.subheader(f"Fat - {order}  Foods (100 g) ")
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(sorted_df['Desc'], sorted_df['Fat_g'], color='#ffdd00' )
    ax.set_xlabel('Fat (g)')
    ax.invert_yaxis()  # To display the highest at the top

    # Annotating the bars with fat amounts inside the bars
    for bar, desc in zip(bars, sorted_df['FoodName']):
    # Annotating the carb amount
        ax.text(
            bar.get_width() - 0.05,  # Position text slightly to the left of the bar's end
            bar.get_y() + bar.get_height() / 2,  # Center the text vertically on the bar
            f'{bar.get_width():.2f}',  # Format the text (carb amount)
            va='center',  # Vertical alignment
            ha='right',  # Horizontal alignment to keep it inside the bar
            color='black',  # Text color
            fontsize=10,  # Font size
            weight='bold'  # Make the text bold 
        )
        
        ax.text(
            0.05,  
            bar.get_y() + bar.get_height() / 2, 
            desc,  
            va='center',  
            ha='left',  
            color='black',  
            fontsize=10,  
            weight='bold'   
        )
    st.pyplot(fig)