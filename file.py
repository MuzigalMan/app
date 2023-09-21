import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt
from functions import get_ids


try:
    connection = create_engine(
        "mysql+pymysql://doadmin:jujcgqi2qtufrq3z@muzigal-prod-do-user-7549922-0.a.db.ondigitalocean.com:25060/muzigal_prod"
    )
    # connection = create_engine(
    #     "mysql+pymysql://doadmin:z1uhlsyqhmcxpnsc@mz-db-dev-do-user-7549922-0.b.db.ondigitalocean.com:25060/muzigal_prod"
    # )
except Exception as e:
    print("error has occured")


select = st.selectbox('What would you like to perform?',
    ('Select','Add Classes', 'Custom', 'Refund', 'Batch Settlement'))
 

if select == 'Add Classes':
    
    id = st.text_input("Order ID*")
    
    payment_id = st.text_input("Payment Id*")
    
    submited =  st.button("Make Changes")
        
    if submited:
        
        if id and payment_id is not None:
        
            query = f"UPDATE muzigal_prod.orders SET razorpay_payment_id = '{payment_id}' , payment_complete = 1 WHERE id = {id};"
            
            try:
                connection.execute(query)
            except Exception as e:
                print(f"Error has occured:{e}")
            finally:
                st.write("Changes Done!")
        
        else:
                st.write("Enter Values")
                
elif select == 'Custom':
    
    id = st.text_input("Order Id*")
    
    classes = st.text_input("Classes")
    
    amount = st.number_input("Amount")
    
    submited = st.button("Make Changes")
    
    if submited:
        
        if id is not None:
            
            if classes is not None and amount is None:
                query = f"UPDATE muzigal_prod.orders SET  session_qty = {classes} WHERE id = {id};"
            elif amount is not None and classes is None:
                query = f"UPDATE muzigal_prod.orders SET  amount = {amount} WHERE id = {id};"
            elif classes and amount is not None:
                query = f"UPDATE muzigal_prod.orders SET  session_qty = {classes},amount = {amount}  WHERE id = {id};"
            
            try:
                connection.execute(query)
            except Exception as e:
                print(f"Error has occured:{e}")
            finally:
                st.write("Changes Done!")
        
        else:
            st.write("Enter Values")
    
elif select == 'Refund':
    
    id = st.text_input("Order ID*")
        
    refund_amount = st.number_input("Refund Amount*")
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
            
            note = f'Original order: {amount}; Refund amount: {refund_amount} | Reason: {notes}'
            
            query = f"UPDATE muzigal_prod.orders SET session_qty = {completed_classes}, amount = {new_amount}, notes = '{note}', refund_amount = {refund_amount}, refund_date = '{dt.now()}' WHERE id = {id};"
            
            
            try:
                connection.execute(query)
            except Exception as e:
                print(f"Error has occured:{e}")
            finally:
                st.markdown("Changes Done!")
                
    else:
        st.write("Please Enter Values")
        
elif select == 'Batch Settlement':
    
    mark_complete_file = st.file_uploader("Upload Mark Complete CSV file", accept_multiple_files=False)
    
    add_back_file = st.file_uploader("Upload Add Back CSV File", accept_multiple_files=False)
    
    col1, col2 = st.columns([3,3])
    
    with col1:
        batch_start_date = st.date_input("Batch start date", dt.date(dt.now()))
    
    with col2:
        batch_end_date = st.date_input("Batch end date", dt.date(dt.now()))
    
    submited =  st.button("Create Batch")
    
    if submited:
        
        if mark_complete_file and add_back_file and batch_start_date and batch_end_date is not None:
        
            mc_ids = get_ids(mark_complete_file)
            
            ab_ids = get_ids(add_back_file)
            
            class_mark_completion = f"""SET SQL_SAFE_UPDATES = 0;
                                        UPDATE class_schedule SET is_complete=1 WHERE id IN {mc_ids}; 
                                        SET SQL_SAFE_UPDATES = 1;
                                        """
                                        
            log_classes_before_deletion = f"""INSERT INTO slot_cancel_log(slot_id,slot_type,student_id,class_id,order_id,reason,created_date)
                                                SELECT slot_id,1,student_id,id,order_id,'System mark completion with Auto process',NOW() FROM class_schedule
                                                WHERE id IN {ab_ids};"""
                                                
            delete_incomplete_classes = f"""DELETE FROM class_schedule WHERE id IN {ab_ids};"""
                                            
            create_batch = f"""CALL `muzigal_prod`.`batch_summary_pr`('{batch_start_date}','{batch_end_date}');"""
            
            average_report = """SELECT 
                                SUM(net_amount),
                                MIN(net_amount),
                                MAX(net_amount),
                                AVG(net_amount),
                                count(case when currency = 'INR' then net_amount end) as INR,
                                count(case when currency = 'USD' then net_amount end) as US,
                                COUNT(net_amount) AS total_count
                            FROM batch_transactions a
                            INNER JOIN teacher_profile b ON a.teacher_id = b.users_id
                            WHERE batch_id = (select batch_id from batch_transactions order by id desc limit 1) AND b.zone_id = 1 AND net_amount != 0;
                            """
                            
            queries = [class_mark_completion,log_classes_before_deletion,delete_incomplete_classes,create_batch]
            
            for i in range(len(queries)):
                try:
                    # connection.execute(queries[i])
                    st.markdown(queries[i])
                except Exception as e:
                    st.markdown(f"Error has occured:{e}")

            st.markdown(f"Batch Created")
                    
            show_report = pd.read_sql_query(average_report,connection)
            
            st.table(show_report)
            
        else:
            st.write("Enter Values")