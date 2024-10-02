# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customise Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# option = st.selectbox('What is your favorite fruit?',('Banana','Strawberries', 'Peaches'))
# st.write('You selected', option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('Name on the Smoothie will be: ',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 Ingredients:', my_dataframe, max_selections =5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen

    # st.write(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")

# if ingredients_list is not null: then do everything below this line that is indented.

# new section to display fruitvise nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
fv_df = st.dataframe(data = fruitvise_response.json(), use_container_width = true
