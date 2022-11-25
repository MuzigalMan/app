import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt


try:
    connection = create_engine("mysql+pymysql://doadmin:jujcgqi2qtufrq3z@muzigal-prod-do-user-7549922-0.a.db.ondigitalocean.com:25060/muzigal_prod")
except Exception as e:
    print('error has occured')


select = st.selectbox('What would you like to perform?',
    ('Select','Add Classes', 'Refund'))
 

if select == 'Add Classes':
    
    order = st.text_input("Order ID")
    
    classes = st.number_input("Enter Classes")
    classes = int(classes)
    
    amount = st.number_input("Amount")
    amount = int(amount)
    
    payment_id = st.text_input("Payment Id")
    
    submited =  st.button("Make Changes")
        
    if submited:
        
        if order and classes and amount is not None:
            
            orders_query = f"SELECT * FROM orders WHERE id = {order};"
    
            orders = pd.read_sql_query(orders_query,connection)
            
            total_classes = orders['session_qty']
            
            new_classes = total_classes+classes
            
            new_amount = classes*amount
            
            final_amount = orders['amount']+new_amount
        
            query = f"UPDATE muzigal_prod.orders SET  session_qty = {new_classes}, amount = {final_amount}, razorpay_payment_id = {payment_id} WHERE id = {order};"
            
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