
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from Main import combined_data

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop(['pm2.5', 'pm10'], axis=1), df[['pm2.5', 'pm10']], test_size=0.2, random_state=42)

# Train the linear regression model
lr = LinearRegression()
lr.fit(X_train, y_train)

# Make predictions on the test set
y_pred = lr.predict(X_test)

# Evaluate the model performance
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)