import pandas as pd
from sklearn.model_selection import train_test_split
import constants as ct


cnx,cursor = ct.connectdb()
query = """SELECT * FROM AB
            ORDER BY date DESC"""
df = pd.read_sql(query, con=cnx)
ct.commitdb(cnx , cursor)
# df = df.set_index('date')

df.to_csv('E:/data  pcd/AB.csv', index=False)
print(df)

train_data, test_data = train_test_split(df, test_size=0.2, shuffle=False)

import h2o
h2o.init()


# import autokeras as ak
#
# # Define the input shape of your data
# input_shape = (train_data.shape[1],)
#
# # Initialize the time series regressor
# reg = ak.TimeseriesForecaster(
#     lookback=10,
#     predict_from=1,
#     max_trials=10,
#     objective="val_loss",
#     project_name="stock_prices"
# )
#
# # Fit the model to the training data
# reg.fit(x=train_data.values, y=train_data.values, epochs=100, validation_split=0.2)
#
# # Evaluate the model on the test data
# mae, _ = reg.evaluate(x=test_data.values, y=test_data.values)
# print(f'Mean Absolute Error: {mae:.2f}')
