import streamlit as st
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt


try:
    connection = create_engine("mysql+pymysql://doadmin:z1uhlsyqhmcxpnsc@mz-db-dev-do-user-7549922-0.b.db.ondigitalocean.com:25060/muzigal_prod")
except Exception as e:
    print('error has occured')


select = st.selectbox('What would you like to be performed?',
    ('Add/Reduce Classes', 'Refund'))


if select == 'Add/Reduce Classes':
    
    order = st.text_input("Order ID")
    if order is None:
        st.write("Please Enter Values")
    
    classes = st.text_input("Enter Classes")
    if classes is None:
        st.write("Please Enter Values")
    
    submited =  st.button("Make Changes")
        
    if submited:
        
        query = f"UPDATE muzigal_prod.orders SET  session_qty = {classes}  WHERE id = {order};"
        
        try:
            connection.execute(query)
        except Exception as e:
            print(f"Error has occured:{e}")
        finally:
            st.write("Changes Done!")
    
        
elif select == 'Refund':
        
    id = st.text_input("Order ID")
    if id is None:
        st.write("Please Enter Values")
    
    classes = st.text_input("Enter Classes")
    if classes is None:
        st.write("Please Enter Values")

    bamount = st.number_input("Total Amount")
    bamount = int(bamount)
    if bamount is None:
        st.write("Please Enter Values")

    ramount = st.number_input("Refund Amount")
    ramount = int(ramount)
    if ramount is None:
        st.write("Please Enter Values")
    
    submited = st.button("Make Changes")

    refund = bamount - ramount
    
    note = f'Original order: {bamount}; Refund amount: {refund}'
    
    query = f"UPDATE muzigal_prod.orders SET session_qty = {classes}, amount = {refund}, notes = '{note}', refund_amount = {refund}, refund_date = {dt.now()} WHERE (id = {id})"
    
    
    if submited :
        try:
            connection.execute(query)
        except Exception as e:
            print(f"Error has occured:{e}")
        finally:
            st.markdown("Changes Done!")