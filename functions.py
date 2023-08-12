import pandas as pd

def get_ids(csv):
    
    df = pd.read_csv(csv)
    ids = df['id']
    
    return tuple(id)