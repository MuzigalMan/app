import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt


try:
    connection = create_engine("mysql+pymysql://doadmin:jujcgqi2qtufrq3z@muzigal-prod-do-user-7549922-0.a.db.ondigitalocean.com:25060/muzigal_prod")
except Exception as e:
    print('error has occured')


select = st.selectbox('What would you like to perform?',
    ('Select','Add Classes', 'Reduce Classes', 'Refund'))
 

if select == 'Add Classes':
    
    id = st.text_input("Order ID")
    
    classes = st.number_input("Enter Classes")
    classes = int(classes)
    
    amount = st.number_input("Amount")
    amount = int(amount)
    
    payment_id = st.text_input("Payment Id")
    
    submited =  st.button("Make Changes")
        
    if submited:
        
        if id and classes is not None:
            
            if  amount or payment_id is not None:
            
                orders_query = f"SELECT * FROM orders WHERE id = {id};"
        
                orders = pd.read_sql_query(orders_query,connection)
                
                total_classes = int( orders['session_qty'])
                
                new_classes = total_classes+classes
            
                query = f"UPDATE muzigal_prod.orders SET  session_qty = {new_classes}, amount = {amount}, razorpay_payment_id = '{payment_id}' WHERE id = {id};"
                
                try:
                    connection.execute(query)
                except Exception as e:
                    print(f"Error has occured:{e}")
                finally:
                    st.write("Changes Done!")
                    
            elif amount or payment_id is None:
                
                orders_query = f"SELECT * FROM orders WHERE id = {id};"
        
                orders = pd.read_sql_query(orders_query,connection)
                
                total_classes = int( orders['session_qty'])
                
                new_classes = total_classes+classes
                
                table_amount = int(orders['amount'])
                
                table_payment_id = str(orders['razorpay_payment_id'])
            
                query = f"UPDATE muzigal_prod.orders SET  session_qty = {new_classes}, amount = {table_amount}, razorpay_payment_id = '{table_payment_id}' WHERE id = {id};"
                
                try:
                    connection.execute(query)
                except Exception as e:
                    print(f"Error has occured:{e}")
                finally:
                    st.write("Changes Done!")
        
            else:
                st.write("Enter Values")
                
elif select == 'Reduce Classes':
    
    id = st.text_input("Order Id")
    
    classes = st.text_input("Classes")
    
    submited = st.button("Make Changes")
    
    if submited:
        
        if id and classes is not None:
            
            query = f"UPDATE muzigal_prod.orders SET  session_qty = {classes} WHERE id = {id};"
            
            try:
                connection.execute(query)
            except Exception as e:
                print(f"Error has occured:{e}")
            finally:
                st.write("Changes Done!")
        
        else:
            st.write("Enter Values")
    
elif select == 'Refund':
    
    id = st.text_input("Order ID")
        
    refund_amount = st.number_input("Refund Amount")
    refund_amount = int(refund_amount)
    
    notes = st.text_input("Note")
        
    submited = st.button("Make Changes")
    
    if submited:
        
        if id and refund_amount is not None:
            
            orders_query = f"SELECT * FROM orders WHERE id = {id};"
    
            orders = pd.read_sql_query(orders_query,connection)
            
            total_classes = int( orders['session_qty'])

            amount = int(orders['amount'])
            
            classes_query = f"SELECT count(*) as cc FROM muzigal_prod.class_schedule where order_id = {id};"

            classes = pd.read_sql_query(classes_query,connection)

            completed_classes = int(classes['cc'])

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