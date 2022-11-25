import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt


try:
    connection = create_engine("mysql+pymysql://doadmin:jujcgqi2qtufrq3z@muzigal-prod-do-user-7549922-0.a.db.ondigitalocean.com:25060/muzigal_prod")
except Exception as e:
    print('error has occured')
    
orders_query = f"SELECT * FROM orders WHERE id = 4;"

orders = pd.read_sql_query(orders_query,connection)

total_classes = orders['session_qty']

amount = orders['amount']

per_class_amount = round(orders['amount']//orders['session_qty'],0)

classes_query = f"SELECT count(*) as cc FROM muzigal_prod.class_schedule where order_id = 4;"

classes = pd.read_sql_query(classes_query,connection)

completed_classes = classes['cc']

refund_amount = (total_classes-completed_classes)*per_class_amount

new_amount = amount-refund_amount