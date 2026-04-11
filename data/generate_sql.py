import pandas as pd
import numpy as np

base_path = '/home/sakthi/dbx_projects/restaurant_analytics/00_synthetic_data/data/'

files = [
    base_path + 'restaurants.csv', 
    base_path + 'menu_items.csv', 
    base_path + 'customers.csv', 
    base_path + 'customer_reviews.csv', 
    base_path + 'historical_orders.csv'
]

output_file = base_path + 'insert_all_data.sql'

with open(output_file, 'w', encoding='utf-8') as f:
    for file in files:
        table_name = file.split('/')[-1].replace('.csv', '')
        df = pd.read_csv(file)
        
        # Replace NaN values with SQL NULL
        df = df.replace({np.nan: 'NULL'})
        
        f.write(f"-- Data for {table_name}\n")
        
        for index, row in df.iterrows():
            values = []
            for val in row:
                if val == 'NULL':
                    values.append("NULL")
                elif isinstance(val, str):
                    # Escape single quotes for SQL
                    clean_val = val.replace("'", "''")
                    values.append(f"'{clean_val}'")
                else:
                    values.append(str(val))
            
            row_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(values)});\n"
            f.write(row_sql)
            
        f.write("\n")
        
print("Successfully generated insert_all_data.sql")