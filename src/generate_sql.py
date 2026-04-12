import pandas as pd
import numpy as np
from pathlib import Path

base_path = Path(__file__).resolve().parent
print(base_path)


file_names = [
     'restaurants.csv', 
     'menu_items.csv', 
     'customers.csv', 
     'customer_reviews.csv', 
     'historical_orders.csv'
]

output_file = base_path / 'insert_all_data.sql'
batch_size = 1000  # Adjust based on your DB limits

with open(output_file, 'w', encoding='utf-8') as f:
    for file in file_names:
        table_name = file
        file_path = str(base_path) + "/data/" + file
        df = pd.read_csv(file)
        
        # Replace NaN values with None (which becomes NULL)
        df = df.replace({np.nan: None})
        
        columns = ', '.join(df.columns)
        f.write(f"-- Data for {table_name}\n")
        
        # Process rows in batches
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i : i + batch_size]
            all_row_values = []

            for _, row in batch.iterrows():
                formatted_values = []
                for val in row:
                    if val is None:
                        formatted_values.append("NULL")
                    elif isinstance(val, str):
                        clean_val = val.replace("'", "''")
                        formatted_values.append(f"'{clean_val}'")
                    else:
                        formatted_values.append(str(val))
                
                all_row_values.append(f"({', '.join(formatted_values)})")

            # Combine all rows into a single INSERT statement for this batch
            sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES \n" + ",\n".join(all_row_values) + ";\n\n"
            f.write(sql_statement)
        
        f.write("\n")
        
print(f"Successfully generated {output_file}")