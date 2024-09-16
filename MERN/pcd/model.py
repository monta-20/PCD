import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch
from transformers import CamembertForMaskedLM, CamembertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
import joblib
import constants as ct
sequence_length = 60
def FetchAndPrepare(name="ab"):
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="pcd"
    )

    # Define the query to fetch the 'ab' table data
    query = f"""WITH ab_unique AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY date ORDER BY date) AS row_num
            FROM {name}),
            usdtnd_unique AS (
                SELECT *,
                       ROW_NUMBER() OVER (PARTITION BY date ORDER BY date) AS row_num
                FROM usdtnd)
            SELECT
                ab_unique.*,
                usdtnd_unique.close as dt
            FROM
                ab_unique
            LEFT JOIN
                usdtnd_unique ON ab_unique.date = usdtnd_unique.date
            WHERE
                ab_unique.row_num = 1 AND (usdtnd_unique.row_num = 1 OR usdtnd_unique.row_num IS NULL);
            """

    # Read the data from the MySQL database into a pandas DataFrame
    data = pd.read_sql(query, connection)

    # Close the database connection
    connection.close()

    # Define a function to convert the string to a list
    def str_to_list(string):
        return [int(x) for x in string.strip("[]").split(",")]

    # Apply the function to the 'news_vectors' column and overwrite it with the list format
    data["news_vectors"] = data["news_vectors"].apply(str_to_list)
    # Convert the 'date' column to a datetime data type
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values(by='date', ascending=True)
    data['news'].fillna("", inplace=True)
    data[['date', 'high', 'low', 'close', 'open' , 'dt']] = data[['date', 'high', 'low', 'close', 'open', 'dt']].fillna(
        method='bfill')
    data = data.dropna()
    data.reset_index(drop=True, inplace=True)

    # Convert news_vector to multiple columns
    news_df = data["news_vectors"].apply(pd.Series)
    news_df = news_df.rename(columns=lambda x: f"news_vectors{x}")

    # Concatenate news_df with the original data and drop unnecessary columns
    data = pd.concat([data, news_df], axis=1)
    return data
def ForcastNext5Days(name):
    # Load the model
    model = load_model(f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_model.h5")
    # Load the scaler
    scaler = joblib.load(f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_scaler.pkl")

    data  = FetchAndPrepare()
    data = data.drop(["date", "news", "news_vectors"], axis=1)
    # Scale the data
    data_scaled = scaler.transform(data)
    # Forecast stock price for the next 5 days
    last_sequence = np.array(data_scaled[-sequence_length:])
    next_5_days = []
    for _ in range(5):
        prediction = model.predict(last_sequence.reshape(1, sequence_length, -1))[0][0]
        next_5_days.append(prediction)
        last_sequence = np.vstack([last_sequence[1:], np.append(prediction, np.zeros(data.shape[1] - 1))])

    next_5_days_inv = scaler.inverse_transform(
        np.c_[np.array(next_5_days).reshape(-1, 1), np.zeros((len(next_5_days), data.shape[1] - 1))])[:, 0]
    return  next_5_days_inv
def save_forecast_to_db(name, forecast):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="pcd"
    )

    cursor = connection.cursor()

    # Check if the table exists, if not, create it
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}_forecast ("
                   f"id INT AUTO_INCREMENT PRIMARY KEY, "
                   f"day_1 FLOAT, "
                   f"day_2 FLOAT, "
                   f"day_3 FLOAT, "
                   f"day_4 FLOAT, "
                   f"day_5 FLOAT, "
                   f"created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    # Insert the forecasts into the table
    cursor.execute(f"INSERT INTO {name}_forecast (day_1, day_2, day_3, day_4, day_5) "
                   f"VALUES (%s, %s, %s, %s, %s)", (forecast[0], forecast[1], forecast[2], forecast[3], forecast[4]))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
def save_last_date_to_db(name, last_date):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="pcd"
    )

    cursor = connection.cursor()

    # Check if the table exists, if not, create it
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}_last_date ("
                   f"id INT AUTO_INCREMENT PRIMARY KEY, "
                   f"last_date DATE, "
                   f"created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    # Insert the last date into the table
    cursor.execute(f"INSERT INTO {name}_last_date (last_date) VALUES (%s)", (last_date,))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
def get_latest_date_from_db(name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="pcd"
    )

    cursor = connection.cursor()

    # Fetch the latest date from the database
    cursor.execute(f"SELECT last_date FROM {name}_last_date ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is not None:
        return result[0]
    else:
        return None


def train_model_on_new_data(name):
    import tensorflow as tf
    tf.config.run_functions_eagerly(True)
    print(f"*************** {name} **************")
    # Fetch the latest date from the database
    last_date = get_latest_date_from_db(name)

    if (last_date==None):
        print(f"last date of {name} is NULL")
        return

        # Convert last_date to datetime
    last_date = pd.to_datetime(datetime.combine(last_date, datetime.min.time()))
    # Fetch and prepare data
    data = FetchAndPrepare(name)

    # Filter data to include only dates greater than the last_date and non-null "close" values
    data = data[(data['date'] > last_date) & (~data['close'].isnull())]

    # Convert 'date' column to numpy datetime64 type
    data['date'] = pd.to_datetime(data['date'])

    data = data.drop(["date", "news", "news_vectors"], axis=1)

    if len(data) == 0:
        print(f"No new data for {name}. Skipping...  and last_date={last_date}")
        return

    # Prepare data
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Split into train and test
    train_size = int(len(data) * 0.8)
    train_data = data_scaled[:train_size]
    test_data = data_scaled[train_size:]

    # Create sequences
    def create_sequences(data, sequence_length):
        x, y = [], []
        for i in range(len(data) - sequence_length - 1):
            x.append(data[i: i + sequence_length])
            y.append(data[i + sequence_length, 0])
        return np.array(x), np.array(y)

    sequence_length =1
    x_train, y_train = create_sequences(train_data, sequence_length)
    x_test, y_test = create_sequences(test_data, sequence_length)

    print(x_train)

    # Load the model
    model = load_model(f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_model.h5")


    print(data)
    print(f"x_train shape: {x_train.shape}, type: {x_train.dtype}")
    print(f"y_train shape: {y_train.shape}, type: {y_train.dtype}")
    print(f"x_test shape: {x_test.shape}, type: {x_test.dtype}")
    print(f"y_test shape: {y_test.shape}, type: {y_test.dtype}")

    # Train the model on new data
    history = model.fit(x_train, y_train, batch_size=64, epochs=10, validation_data=(x_test, y_test))

    # Save the updated model
    model.save(f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_model.h5")

    # Update the last_date in the database
    new_last_date = data.loc[data['close'].notnull(), 'date'].max()
    save_last_date_to_db(name, new_last_date)

    print(f"Model for {name} trained on new data and saved.")


def CreatModel(name):
    print(f"*************** {name} **************")
    data   = FetchAndPrepare(name)
    last_date = data.loc[data['close'].notnull(), 'date'].max()
    data = data.drop(["date", "news", "news_vectors"], axis=1)
    # data = data[['close', 'high', 'low' , 'open']]
    # Save the last date with non-null "close" value
    save_last_date_to_db(name, last_date)

    # Prepare data
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    # Split into train and test
    train_size = int(len(data) * 0.8)
    train_data = data_scaled[:train_size]
    test_data = data_scaled[train_size:]
    # Create sequences
    def create_sequences(data, sequence_length):
        x, y = [], []
        for i in range(len(data) - sequence_length - 1):
            x.append(data[i : i + sequence_length])
            y.append(data[i + sequence_length, 0])
        return np.array(x), np.array(y)

    x_train, y_train = create_sequences(train_data, sequence_length)
    x_test, y_test = create_sequences(test_data, sequence_length)

    # Build model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mean_squared_error")
    history  = model.fit(x_train, y_train, batch_size=64, epochs=ct.EPOCHS_TRAIN, validation_data=(x_test, y_test))



    plt.figure(figsize=(12, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Function Over Time')
    plt.legend()
    plt.show()

    # Make predictions
    predictions = model.predict(x_test)
    # Inverse scaling
    y_test_inv = scaler.inverse_transform(np.c_[y_test.reshape(-1, 1), np.zeros((len(y_test), data.shape[1] - 1))])[:, 0]
    predictions_inv = scaler.inverse_transform(np.c_[predictions.reshape(-1, 1), np.zeros((len(predictions), data.shape[1] - 1))])[:, 0]

    # Plot results
    plt.figure(figsize=(16, 8))
    plt.plot(y_test_inv, label="True Values")
    plt.plot(predictions_inv, label="Predictions")
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()

    # Metrics
    mse = mean_squared_error(y_test_inv, predictions_inv)
    mae = mean_absolute_error(y_test_inv, predictions_inv)
    mape = np.mean(np.abs((y_test_inv - predictions_inv) / y_test_inv)) * 100
    print(f"{name} Mean Squared Error (MSE): {mse}")
    print(f"{name} Mean Absolute Error (MAE): {mae}")
    print(f"{name} Mean Absolute Percentage Error (MAPE): {mape}%")


    # Train the model with test data
    x_all, y_all = create_sequences(data_scaled, sequence_length)

    model.fit(x_all, y_all, batch_size=64, epochs=ct.EPOCHS_ALL)
    # # Optional: plot the next 5 days predictions
    # plt.figure(figsize=(10, 5))
    # plt.plot(next_5_days_inv, label="Next 5 Days Predictions")
    # plt.xlabel("Days")
    # plt.ylabel("Stock Price")
    # plt.legend()
    # plt.show()

    model.save(f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_model.h5")

    # Save the scaler
    joblib.dump(scaler, f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_scaler.pkl")
def UpdateAllModels():
    for name in ct.companyNames:
        CreatModel(name)
def UpdateAllForcast():
    for name in ct.companyNames:
        forecast = ForcastNext5Days(name)
        save_forecast_to_db(name, forecast)
        print(f"Forecast for {name} saved to the database.")


def Evaluate(name):
    model = load_model(f"C:/Users/Mohammed Rabia/PycharmProjects/pcd_data_collection/pcd/models/{name}_model.h5")
    plt.figure(figsize=(12, 6))
    plt.plot(model.history['loss'], label='Training Loss')
    plt.plot(model.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Function Over Time')
    plt.legend()
    plt.show()


# Evaluate("BIAT")
CreatModel("BIAT")


# train_model_on_new_data("ab")
# UpdateAllForcast()
# forecast = ForcastNext5Days("ab")
# save_forecast_to_db("ab", forecast)
# print(f"Forecast for ab saved to the database.")