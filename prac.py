import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt


try:
    connection = create_engine("mysql+pymysql://doadmin:jujcgqi2qtufrq3z@muzigal-prod-do-user-7549922-0.a.db.ondigitalocean.com:25060/muzigal_prod")
except Exception as e:
    print('error has occured')
    
orders_query = f"SELECT * FROM orders WHERE id = 121456;"

orders = pd.read_sql_query(orders_query,connection)

classes = 4

total_classes = int(orders['session_qty'])
            
new_classes = total_classes+classes

amount = 0

payment_id = None

query = f"UPDATE muzigal_prod.orders SET  session_qty = {new_classes}, amount = {amount}, razorpay_payment_id = {payment_id} WHERE id = {id};"

print(query)