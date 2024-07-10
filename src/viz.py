import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to the database
engine = create_engine('sqlite:///stocks.db')
df = pd.read_sql('historical_data', con=engine)

# Plot data
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['close'], label='Close Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Close Price Over Time')
plt.legend()
plt.show()
