
import pandas as pd
from etl.transform.transform import transform_facts

df = pd.DataFrame(transform_facts())

output_path='fact_table.csv'
df.to_csv(output_path,index=False)