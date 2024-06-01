import streamlit as st
import pandas as pd
import table
import table2

from streamlit_lottie import st_lottie
import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

logo = load_lottiefile("intro.json")

# Set page title, icon and layout
st.set_page_config(page_title="Health Tracker", layout="wide")


if __name__ == '__main__':
    # Main title for the application
    st.markdown("<h1 style='text-align: center;'>AI Health Tracker</h1>", unsafe_allow_html=True)
    c_11,c_22,c_33 = st.columns([2,1,2])
    with c_22:
        st_lottie(logo, speed=1, width=200, height=200, key="initial")
    
    # Using columns to layout the buttons
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        with st.expander("Login"):
            st.header("Login")
            username_input = st.text_input("username")

            data = table2.entity_retrieve(username_input)
            
            if st.button("Login"):
                age,gender = table.entity_retrieve(username_input)
                if age is not None:
                    if data is not None:
                        st.success("User logged in successfully!")

                    else:
                        st.success("User is registered successfully!")
                        st.info("User data not found! Please Go to astma tracker to track the health symptoms!")
                        
                else:
                    st.error("User not found!")
            if data is not None:
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
                df['date'] = df['date'].dt.strftime('%a %d')
                df = df.set_index('date')
                    
        
        with st.expander("Register"):
            st.header("User Registration")
            register_username = st.text_input("Username")
            age = st.text_input("Age")
            gender = st.selectbox("Gender", ['<Select>', 'Male', 'Female'], index=0)
            
            if st.button("Register"):
                # Perform registration logic here (replace with actual registration logic)
                # e.g., validate inputs, save user to database, etc.
                table.entity_update(register_username, age, gender)
                st.success("User registered successfully!")
                st.info("Please login to continue!")
    if data is not None:
        user_age, user_gender = table.entity_retrieve(username_input)
        with st.expander("Dashboard"):
            st.header("Dashboard")
        # Display dashboard content here
            c_1,c_2,c_3 = st.columns([1,1,1])
            with c_1:
                st.success(f"Name : {username_input}")
            with c_2:
                st.info(f"Age : {user_age}")
            with c_3:
                st.warning(f"Gender : {user_gender}")
            st.line_chart(df['severity'])

