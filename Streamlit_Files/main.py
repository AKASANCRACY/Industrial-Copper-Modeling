import streamlit as st
import numpy as np
import joblib
import pickle
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Price Predictor",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )
st.markdown("<h1 style='text-align: center; color: red;'>Industrial Copper Modeling</h1>", unsafe_allow_html=True)

# SETTING-UP BACKGROUND IMAGE
st.markdown(f""" 
            <style>
            .stApp {{
            background: #bba0db;
            background-size: cover;
            transition: background 0.5s ease;
            }}
            .stButton>button {{
            color: white;
            background-color: black;
        }}
            .stAlert.success {{
            color: white;
        background-color: black;
        }}
            </style>
            """,unsafe_allow_html=True)

options = option_menu(None, ["Regression","Classification"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "25px", "text-align": "centre", "margin": "0px", "--hover-color": "red", "transition": "color 0.3s ease, background-color 0.3s ease"},
                               "container" : {"max-width": "6000px", "padding": "10px", "border-radius": "5px"},
                               "nav-link-selected": {"background-color": "red", "color": "white"}})


col1, col2 = st.columns(2)
with col1:
    quantity_tons = st.number_input('Quantity Tons', min_value=1)
with col2:
    application = st.number_input('Application' ,min_value=1, step=1)
col3, col4 = st.columns(2)
with col3:
    thickness = st.number_input('Thickness' ,min_value=0.1)
with col4:
    width = st.number_input('Width' ,min_value=0.1)
col5, col6 = st.columns(2)
with col5:
    country = st.number_input('Country' ,min_value=1 ,step=1)
with col6:
    customer = st.number_input('Customer' ,step=1)
col7, col8 = st.columns(2)
with col7:
    product_ref = st.number_input('Product Ref' ,min_value=1 ,step=1)
with col8:
    item_type = st.selectbox('Item Type', ['W' ,'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR'])

if options == "Regression":
    # Load the model from the file
    with open('Regressor.pkl', 'rb') as file:
        best_model = pickle.load(file)
    
    ohe = joblib.load('ohe.joblib')
    ohe2 = joblib.load('ohe2.joblib')
    scaler = joblib.load('scaler.joblib')

    col9, col10, col11 = st.columns(3)
    with col10:
        status = st.selectbox('Status', ['Won', 'Lost'])

    if st.button("predict"):
        # Prediction of selling price
        new_sample = np.array([[np.log(quantity_tons), application, np.log(thickness), width, country, customer, product_ref, item_type, status]])
        new_sample_ohe = ohe.transform(new_sample[:,[7]]).toarray()
        new_sample_be = ohe2.transform(new_sample[:, [8]]).toarray()
        new_sample = np.concatenate((new_sample[:, [0,1,2, 3, 4, 5, 6,]], new_sample_ohe, new_sample_be), axis=1)
        new_sample1 = scaler.transform(new_sample)
        new_pred = best_model.predict(new_sample1)
        price = str(np.exp(new_pred[0]))
        string = 'Predicted selling price:' + price
        st.success(string)

else:
    # Load the model from the file
    with open('Classifier.pkl', 'rb') as file:
        dtc = pickle.load(file)
    
    ohe = joblib.load('ohec.joblib')
    scaler = joblib.load('scalerc.joblib')

    
    col9, col10, col11 = st.columns(3)
    with col10:
        selling_price = st.number_input('Selling Price' ,min_value=1 ,step=1)
    
    if st.button("predict"):
        #new_sample = np.array([[np.log(quantity_tons), np.log(selling_price), application, np.log(thickness),width,country,customer,product_ref,item_type]])
        new_sample = np.array([[np.log(700), np.log(956), 10, np.log(2),1500,28.0,30202938,1670798778,'W']])
        new_sample_ohe = ohe.transform(new_sample[:, [8]]).toarray()
        new_sample = np.concatenate((new_sample[:, [0,1,2, 3, 4, 5, 6,7]], new_sample_ohe), axis=1)
        new_sample = scaler.transform(new_sample)
        new_pred = dtc.predict(new_sample)
        if new_pred==1:
            st.success('The status is: Won')
        else:
            st.error('The status is: Lost')
