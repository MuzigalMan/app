import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt


try:
    connection = create_engine("mysql+pymysql://doadmin:z1uhlsyqhmcxpnsc@mz-db-dev-do-user-7549922-0.b.db.ondigitalocean.com:25060/muzigal_prod")
except Exception as e:
    print('error has occured')


select = st.selectbox('What would you like to perform?',
    ('Select','Add/Reduce Classes', 'Refund'))
 

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
        
    refund_amount = st.text_input("Refund Amount")
    
    notes = st.text_input("Note")
        
    submited = st.button("Make Changes")
    
    if submited:
        
        if id and refund_amount is not None:
            
            orders_query = f"SELECT * FROM orders WHERE id = {id};"
    
            orders = pd.read_sql_query(orders_query,connection)
            
            total_classes = orders['session_qty']

            amount = orders['amount']
            
            classes_query = f"SELECT count(*) as cc FROM muzigal_prod.class_schedule where order_id = {id};"

            classes = pd.read_sql_query(classes_query,connection)

            completed_classes = classes['cc']

            new_amount = amount-refund_amount
            
            note = f'Original order: {amount}; Refund amount: {refund_amount} | {notes}'
            
            query = f"UPDATE muzigal_prod.orders SET session_qty = {completed_classes}, amount = {new_amount}, notes = '{note}', refund_amount = {refund_amount}, refund_date = '{dt.now()}' WHERE id = {id};"
            
            
            try:
                connection.execute(query)
            except Exception as e:
                print(f"Error has occured:{e}")
            finally:
                st.markdown("Changes Done!")
                
    else:
        st.write("Please Enter Values")