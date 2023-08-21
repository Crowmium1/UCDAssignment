# Import necessary modules
import requests
import pandas as pd

# Define the API key and URL for the weather data
api_key = '7849f9e9237e45dc822145438231704'
city = 'Galway'
start_date = '2023-04-01'
end_date = '2023-04-16'

# Create an empty DataFrame to store the extracted data
weather_data = pd.DataFrame()

# Use a for loop to iterate over each day in the date range
for i, date in enumerate(pd.date_range(start_date, end_date)):
    # Create the API URL for the current date
    url = f'http://api.weatherapi.com/v1/history.json?key={api_key}&q={city}&dt={date.strftime("%Y-%m-%d")}'

    # Query the API and extract necessary data
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        daily_forecast = pd.DataFrame(data['forecast']['forecastday'][0]['day'])

        unwanted_columns = ['maxtemp_f', 'mintemp_f', 'avgtemp_f', 'maxwind_mph', 'totalprecip_in', 'avgvis_miles',
                            'condition']
        #Remove unwanted rows and columns
        daily_forecast.drop(columns=unwanted_columns, inplace=True)
        daily_forecast.drop(index=['code', 'icon'], inplace=True)

        #Resetting index
        daily_forecast = daily_forecast.reset_index().rename(columns={'index': 'day'}).set_index(['day', pd.Index([i])])

        # Append the extracted data to the DataFrame
        weather_data = pd.concat([weather_data.reset_index(drop=True), daily_forecast], axis=0)

    else:
        print("Error:", response.status_code, response.text)

# Display the final DataFrame
print(weather_data)


#Pollution Data for Briarhill, Co.Galway
import pandas as pd

# Specify the CSV file name and delimiter
file_name = 'AirQuality.csv'
delimiter = ','

# Read the first 5 rows of the CSV file
df_pollution = pd.read_csv(file_name, delimiter=delimiter, header=0, nrows=15)

# Select the desired columns using the .iloc method
df_pollution = df_pollution.iloc[:, 0:4]

# Print the resulting DataFrame
print(df_pollution)

#Combining pollution and weather dataframes #Rename the columns of the pollution dataframe
# Rename the columns of the pollution dataframe
#weather_data.insert(0, 'day', '')
df_pollution.columns = ['day', 'pm2.5', 'pm10', 'NO3']

# Merge the dataframes
combined_data = pd.merge(weather_data.reset_index(), df_pollution.reset_index(), how='outer', left_index=True, right_index=True)

#Remove last two rows, as there is an error in the code still with the tuple showing up in the index.
combined_data = combined_data.drop(combined_data.tail(2).index)

# View Columns remaining
for col in combined_data.columns:
    print(col)

#Remove unneeded columns
combined_data.drop(columns=['index_x','index_y','avgvis_km', 'maxtemp_c', 'mintemp_c', 'uv'], inplace=True)
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 15)

# convert date column to datetime object
combined_data['day'] = pd.to_datetime(combined_data['day'])

# calculate number of days since minimum date
combined_data['day'] = (combined_data['day'] - combined_data['day'].min()).dt.days + 1

print(combined_data)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

training_data = combined_data.drop(columns=['day'])

X = training_data.drop(columns=['pm2.5', 'pm10', 'NO3'])
y_pm25 = training_data['pm2.5']
y_pm10 = training_data['pm10']
y_no3 = training_data['NO3']

for i, y in enumerate([y_pm25, y_pm10, y_no3]):
    reg = LinearRegression()
    reg.fit(X, y)
    y_pred = reg.predict(X)
    mse = mean_squared_error(y, y_pred)
    print("MSE for variable ", i+1, ": ", mse)

#Increase the sample size and perform analysis on it
# Assume you have a new dataframe called "new_data" with the same columns as "training_data" with a large sample size.
#X_new = new_data.drop(columns=['pm2.5', 'pm10', 'NO3'])
#y_pm25_pred = reg.predict(X_new)

# print the predicted PM2.5 values
#print(y_pm25_pred)

#Random Forest Regression Modelling
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_pm25, test_size=0.2, random_state=42)

# Train Random Forest model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Test Random Forest model
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("MSE for Random Forest Regression: ", mse)

# Loop through pm2.5, pm10, and NO3
for i, y in enumerate([y_pm25, y_pm10, y_no3]):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Test Random Forest model
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # Print MSE with corresponding variable name
    if i == 0:
        var_name = 'pm2.5'
    elif i == 1:
        var_name = 'pm10'
    else:
        var_name = 'NO3'
    print("MSE for", var_name, "using Random Forest Regression: ", mse)