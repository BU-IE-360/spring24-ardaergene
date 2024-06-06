```python
import pandas as pd

# Load production data
production_df = pd.read_csv('production.csv')

# Load weather data
weather_df = pd.read_csv("processed_weather.csv")

# Convert 'date' column to datetime and 'hour' column to numeric in weather dataframe
weather_df['datetime'] = pd.to_datetime(weather_df['date'] + ' ' + weather_df['hour'].astype(str) + ':00:00')

# Drop unnecessary columns from the weather dataframe
weather_df.drop(['date', 'hour'], axis=1, inplace=True)

# Reshape the weather data to wide format
weather_wide = weather_df.pivot_table(index='datetime', 
                                      columns=['lat', 'lon'], 
                                      values=['dswrf_surface', 'tcdc_low.cloud.layer', 'tcdc_middle.cloud.layer',
                                              'tcdc_high.cloud.layer', 'tcdc_entire.atmosphere', 'uswrf_top_of_atmosphere',
                                              'csnow_surface', 'dlwrf_surface', 'uswrf_surface', 'tmp_surface'],
                                      aggfunc='first')

# Flatten the multi-level column index
weather_wide.columns = ['_'.join(map(str, col)).strip() for col in weather_wide.columns.values]

# Reset the index to make 'datetime' a column again
weather_wide.reset_index(inplace=True)

# Convert 'date' column to datetime and 'hour' column to numeric in production dataframe
production_df['datetime'] = pd.to_datetime(production_df['date'] + ' ' + production_df['hour'].astype(str) + ':00:00')

# Drop unnecessary columns from the production dataframe
production_df.drop(['date', 'hour'], axis=1, inplace=True)

# Merge the reshaped weather data with the production data on the 'datetime' column
merged_data = pd.merge(weather_wide, production_df, on='datetime', how='inner')
merged_data.sort_values(by=['datetime'], inplace=True)

# Filter available data to include only hours with production data
available_data = merged_data[~merged_data['production'].isna()]

# Display the available data
print("Available Data:")
print(available_data.head(10))

```

    Available Data:
                 datetime  csnow_surface_37.75_34.5  csnow_surface_37.75_34.75  \
    0 2022-01-01 04:00:00                       0.0                        0.0   
    1 2022-01-01 05:00:00                       0.0                        0.0   
    2 2022-01-01 06:00:00                       0.0                        0.0   
    3 2022-01-01 07:00:00                       0.0                        0.0   
    4 2022-01-01 08:00:00                       0.0                        0.0   
    5 2022-01-01 09:00:00                       0.0                        0.0   
    6 2022-01-01 10:00:00                       0.0                        0.0   
    7 2022-01-01 11:00:00                       0.0                        0.0   
    8 2022-01-01 12:00:00                       0.0                        0.0   
    9 2022-01-01 13:00:00                       0.0                        0.0   
    
       csnow_surface_37.75_35.0  csnow_surface_37.75_35.25  \
    0                       0.0                        0.0   
    1                       0.0                        0.0   
    2                       0.0                        0.0   
    3                       0.0                        0.0   
    4                       0.0                        0.0   
    5                       0.0                        0.0   
    6                       0.0                        0.0   
    7                       0.0                        0.0   
    8                       0.0                        0.0   
    9                       0.0                        0.0   
    
       csnow_surface_37.75_35.5  csnow_surface_38.0_34.5  \
    0                       0.0                      0.0   
    1                       0.0                      0.0   
    2                       0.0                      0.0   
    3                       0.0                      0.0   
    4                       0.0                      0.0   
    5                       0.0                      0.0   
    6                       0.0                      0.0   
    7                       0.0                      0.0   
    8                       0.0                      0.0   
    9                       0.0                      0.0   
    
       csnow_surface_38.0_34.75  csnow_surface_38.0_35.0  \
    0                       0.0                      0.0   
    1                       0.0                      0.0   
    2                       0.0                      0.0   
    3                       0.0                      0.0   
    4                       0.0                      0.0   
    5                       0.0                      0.0   
    6                       0.0                      0.0   
    7                       0.0                      0.0   
    8                       0.0                      0.0   
    9                       0.0                      0.0   
    
       csnow_surface_38.0_35.25  ...  uswrf_top_of_atmosphere_38.5_34.75  \
    0                       0.0  ...                               0.000   
    1                       0.0  ...                               0.000   
    2                       0.0  ...                               0.000   
    3                       0.0  ...                               0.000   
    4                       0.0  ...                               0.000   
    5                       0.0  ...                               8.368   
    6                       0.0  ...                             102.752   
    7                       0.0  ...                             116.944   
    8                       0.0  ...                             132.480   
    9                       0.0  ...                             148.432   
    
       uswrf_top_of_atmosphere_38.5_35.0  uswrf_top_of_atmosphere_38.5_35.25  \
    0                              0.000                               0.000   
    1                              0.000                               0.000   
    2                              0.000                               0.000   
    3                              0.000                               0.000   
    4                              0.000                               0.000   
    5                              8.704                               8.816   
    6                            120.864                             136.496   
    7                            123.584                             133.936   
    8                            132.176                             138.080   
    9                            141.488                             143.072   
    
       uswrf_top_of_atmosphere_38.5_35.5  uswrf_top_of_atmosphere_38.75_34.5  \
    0                              0.000                               0.000   
    1                              0.000                               0.000   
    2                              0.000                               0.000   
    3                              0.000                               0.000   
    4                              0.000                               0.000   
    5                             12.080                               7.536   
    6                            199.200                             104.464   
    7                            234.032                             140.640   
    8                            259.504                             156.672   
    9                            277.776                             164.368   
    
       uswrf_top_of_atmosphere_38.75_34.75  uswrf_top_of_atmosphere_38.75_35.0  \
    0                                0.000                               0.000   
    1                                0.000                               0.000   
    2                                0.000                               0.000   
    3                                0.000                               0.000   
    4                                0.000                               0.000   
    5                                8.096                               8.592   
    6                              105.264                             120.656   
    7                              127.472                             130.512   
    8                              141.328                             140.320   
    9                              157.712                             161.376   
    
       uswrf_top_of_atmosphere_38.75_35.25  uswrf_top_of_atmosphere_38.75_35.5  \
    0                                0.000                               0.000   
    1                                0.000                               0.000   
    2                                0.000                               0.000   
    3                                0.000                               0.000   
    4                                0.000                               0.000   
    5                                8.848                               8.704   
    6                              137.664                             142.336   
    7                              142.112                             147.088   
    8                              150.656                             150.096   
    9                              168.096                             154.944   
    
       production  
    0        0.00  
    1        0.00  
    2        0.00  
    3        0.00  
    4        3.40  
    5        6.80  
    6        9.38  
    7        7.65  
    8        6.80  
    9        5.10  
    
    [10 rows x 252 columns]
    

I defined traning data in terms of date


```python
# Define the training and test period
train_end_date = '2024-01-31'
test_start_date = '2024-02-01'
test_end_date = '2024-05-15'

# Split the data
train_data = available_data[available_data['datetime'] <= train_end_date]
test_data = available_data[(available_data['datetime'] >= test_start_date) & (available_data['datetime'] <= test_end_date)]

print("Training Data:")
print(train_data.head(10))

print("\nTest Data:")
print(test_data.head(10))

```

    Training Data:
                 datetime  csnow_surface_37.75_34.5  csnow_surface_37.75_34.75  \
    0 2022-01-01 04:00:00                       0.0                        0.0   
    1 2022-01-01 05:00:00                       0.0                        0.0   
    2 2022-01-01 06:00:00                       0.0                        0.0   
    3 2022-01-01 07:00:00                       0.0                        0.0   
    4 2022-01-01 08:00:00                       0.0                        0.0   
    5 2022-01-01 09:00:00                       0.0                        0.0   
    6 2022-01-01 10:00:00                       0.0                        0.0   
    7 2022-01-01 11:00:00                       0.0                        0.0   
    8 2022-01-01 12:00:00                       0.0                        0.0   
    9 2022-01-01 13:00:00                       0.0                        0.0   
    
       csnow_surface_37.75_35.0  csnow_surface_37.75_35.25  \
    0                       0.0                        0.0   
    1                       0.0                        0.0   
    2                       0.0                        0.0   
    3                       0.0                        0.0   
    4                       0.0                        0.0   
    5                       0.0                        0.0   
    6                       0.0                        0.0   
    7                       0.0                        0.0   
    8                       0.0                        0.0   
    9                       0.0                        0.0   
    
       csnow_surface_37.75_35.5  csnow_surface_38.0_34.5  \
    0                       0.0                      0.0   
    1                       0.0                      0.0   
    2                       0.0                      0.0   
    3                       0.0                      0.0   
    4                       0.0                      0.0   
    5                       0.0                      0.0   
    6                       0.0                      0.0   
    7                       0.0                      0.0   
    8                       0.0                      0.0   
    9                       0.0                      0.0   
    
       csnow_surface_38.0_34.75  csnow_surface_38.0_35.0  \
    0                       0.0                      0.0   
    1                       0.0                      0.0   
    2                       0.0                      0.0   
    3                       0.0                      0.0   
    4                       0.0                      0.0   
    5                       0.0                      0.0   
    6                       0.0                      0.0   
    7                       0.0                      0.0   
    8                       0.0                      0.0   
    9                       0.0                      0.0   
    
       csnow_surface_38.0_35.25  ...  uswrf_top_of_atmosphere_38.5_34.75  \
    0                       0.0  ...                               0.000   
    1                       0.0  ...                               0.000   
    2                       0.0  ...                               0.000   
    3                       0.0  ...                               0.000   
    4                       0.0  ...                               0.000   
    5                       0.0  ...                               8.368   
    6                       0.0  ...                             102.752   
    7                       0.0  ...                             116.944   
    8                       0.0  ...                             132.480   
    9                       0.0  ...                             148.432   
    
       uswrf_top_of_atmosphere_38.5_35.0  uswrf_top_of_atmosphere_38.5_35.25  \
    0                              0.000                               0.000   
    1                              0.000                               0.000   
    2                              0.000                               0.000   
    3                              0.000                               0.000   
    4                              0.000                               0.000   
    5                              8.704                               8.816   
    6                            120.864                             136.496   
    7                            123.584                             133.936   
    8                            132.176                             138.080   
    9                            141.488                             143.072   
    
       uswrf_top_of_atmosphere_38.5_35.5  uswrf_top_of_atmosphere_38.75_34.5  \
    0                              0.000                               0.000   
    1                              0.000                               0.000   
    2                              0.000                               0.000   
    3                              0.000                               0.000   
    4                              0.000                               0.000   
    5                             12.080                               7.536   
    6                            199.200                             104.464   
    7                            234.032                             140.640   
    8                            259.504                             156.672   
    9                            277.776                             164.368   
    
       uswrf_top_of_atmosphere_38.75_34.75  uswrf_top_of_atmosphere_38.75_35.0  \
    0                                0.000                               0.000   
    1                                0.000                               0.000   
    2                                0.000                               0.000   
    3                                0.000                               0.000   
    4                                0.000                               0.000   
    5                                8.096                               8.592   
    6                              105.264                             120.656   
    7                              127.472                             130.512   
    8                              141.328                             140.320   
    9                              157.712                             161.376   
    
       uswrf_top_of_atmosphere_38.75_35.25  uswrf_top_of_atmosphere_38.75_35.5  \
    0                                0.000                               0.000   
    1                                0.000                               0.000   
    2                                0.000                               0.000   
    3                                0.000                               0.000   
    4                                0.000                               0.000   
    5                                8.848                               8.704   
    6                              137.664                             142.336   
    7                              142.112                             147.088   
    8                              150.656                             150.096   
    9                              168.096                             154.944   
    
       production  
    0        0.00  
    1        0.00  
    2        0.00  
    3        0.00  
    4        3.40  
    5        6.80  
    6        9.38  
    7        7.65  
    8        6.80  
    9        5.10  
    
    [10 rows x 252 columns]
    
    Test Data:
                     datetime  csnow_surface_37.75_34.5  \
    18259 2024-02-01 00:00:00                       0.0   
    18260 2024-02-01 01:00:00                       0.0   
    18261 2024-02-01 02:00:00                       0.0   
    18262 2024-02-01 03:00:00                       0.0   
    18263 2024-02-01 04:00:00                       0.0   
    18264 2024-02-01 05:00:00                       0.0   
    18265 2024-02-01 06:00:00                       0.0   
    18266 2024-02-01 07:00:00                       0.0   
    18267 2024-02-01 08:00:00                       0.0   
    18268 2024-02-01 09:00:00                       0.0   
    
           csnow_surface_37.75_34.75  csnow_surface_37.75_35.0  \
    18259                        0.0                       0.0   
    18260                        0.0                       0.0   
    18261                        0.0                       0.0   
    18262                        0.0                       0.0   
    18263                        0.0                       0.0   
    18264                        0.0                       0.0   
    18265                        0.0                       0.0   
    18266                        0.0                       0.0   
    18267                        0.0                       0.0   
    18268                        0.0                       0.0   
    
           csnow_surface_37.75_35.25  csnow_surface_37.75_35.5  \
    18259                        0.0                       0.0   
    18260                        0.0                       0.0   
    18261                        0.0                       0.0   
    18262                        0.0                       0.0   
    18263                        0.0                       0.0   
    18264                        0.0                       0.0   
    18265                        0.0                       0.0   
    18266                        0.0                       0.0   
    18267                        0.0                       0.0   
    18268                        0.0                       0.0   
    
           csnow_surface_38.0_34.5  csnow_surface_38.0_34.75  \
    18259                      0.0                       0.0   
    18260                      0.0                       0.0   
    18261                      0.0                       0.0   
    18262                      0.0                       0.0   
    18263                      0.0                       0.0   
    18264                      0.0                       0.0   
    18265                      0.0                       0.0   
    18266                      0.0                       0.0   
    18267                      0.0                       0.0   
    18268                      0.0                       0.0   
    
           csnow_surface_38.0_35.0  csnow_surface_38.0_35.25  ...  \
    18259                      0.0                       0.0  ...   
    18260                      0.0                       0.0  ...   
    18261                      0.0                       0.0  ...   
    18262                      0.0                       0.0  ...   
    18263                      0.0                       0.0  ...   
    18264                      0.0                       0.0  ...   
    18265                      0.0                       0.0  ...   
    18266                      0.0                       0.0  ...   
    18267                      0.0                       0.0  ...   
    18268                      0.0                       0.0  ...   
    
           uswrf_top_of_atmosphere_38.5_34.75  uswrf_top_of_atmosphere_38.5_35.0  \
    18259                               0.000                              0.000   
    18260                               0.000                              0.000   
    18261                               0.000                              0.000   
    18262                               0.000                              0.000   
    18263                               0.000                              0.000   
    18264                               0.000                              0.000   
    18265                               0.000                              0.000   
    18266                               0.000                              0.000   
    18267                               0.224                              0.272   
    18268                              13.008                             13.168   
    
           uswrf_top_of_atmosphere_38.5_35.25  uswrf_top_of_atmosphere_38.5_35.5  \
    18259                               0.000                               0.00   
    18260                               0.000                               0.00   
    18261                               0.000                               0.00   
    18262                               0.000                               0.00   
    18263                               0.000                               0.00   
    18264                               0.000                               0.00   
    18265                               0.000                               0.00   
    18266                               0.000                               0.00   
    18267                               0.320                               0.48   
    18268                              12.304                              17.36   
    
           uswrf_top_of_atmosphere_38.75_34.5  \
    18259                               0.000   
    18260                               0.000   
    18261                               0.000   
    18262                               0.000   
    18263                               0.000   
    18264                               0.000   
    18265                               0.000   
    18266                               0.000   
    18267                               0.128   
    18268                               9.344   
    
           uswrf_top_of_atmosphere_38.75_34.75  \
    18259                                0.000   
    18260                                0.000   
    18261                                0.000   
    18262                                0.000   
    18263                                0.000   
    18264                                0.000   
    18265                                0.000   
    18266                                0.000   
    18267                                0.176   
    18268                                9.920   
    
           uswrf_top_of_atmosphere_38.75_35.0  \
    18259                               0.000   
    18260                               0.000   
    18261                               0.000   
    18262                               0.000   
    18263                               0.000   
    18264                               0.000   
    18265                               0.000   
    18266                               0.000   
    18267                               0.224   
    18268                              10.704   
    
           uswrf_top_of_atmosphere_38.75_35.25  \
    18259                                0.000   
    18260                                0.000   
    18261                                0.000   
    18262                                0.000   
    18263                                0.000   
    18264                                0.000   
    18265                                0.000   
    18266                                0.000   
    18267                                0.288   
    18268                               11.040   
    
           uswrf_top_of_atmosphere_38.75_35.5  production  
    18259                               0.000        0.00  
    18260                               0.000        0.00  
    18261                               0.000        0.00  
    18262                               0.000        0.00  
    18263                               0.000        0.00  
    18264                               0.000        0.00  
    18265                               0.000        0.01  
    18266                               0.000        1.59  
    18267                               0.352        6.17  
    18268                              11.600        7.11  
    
    [10 rows x 252 columns]
    

I'm importing some tools here. So, I've got this auto_arima thing from pmdarima, which helps me pick the best ARIMA model without me having to do all the guesswork. Also, I need mean_squared_error from sklearn.metrics to check how well my models are doing.

Now, I'm setting up this empty dictionary called arima_models to hold all the ARIMA models I'm going to create for each hour.

I'm going through each hour of the day, you know, from 0 to 23. And for each hour, I'm taking the production data for that specific hour from my training dataset.

Then, I'm using auto_arima to automatically select the best ARIMA model for that hour's production data. I don't want any seasonal stuff in this case, so I set seasonal=False.

After that, I'm storing the fitted ARIMA model in my arima_models dictionary, so I can use it later.

Finally, I'm just printing out all the fitted ARIMA models I've got, you know, to see what they look like


Hour 0:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 1:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 2:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 3:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 4:  ARIMA(2,1,4)(0,0,0)[0]          
Hour 5:  ARIMA(2,1,3)(0,0,0)[0]          
Hour 6:  ARIMA(2,1,3)(0,0,0)[0]          
Hour 7:  ARIMA(3,1,3)(0,0,0)[0] intercept
Hour 8:  ARIMA(0,1,3)(0,0,0)[0]          
Hour 9:  ARIMA(2,1,1)(0,0,0)[0]          
Hour 10:  ARIMA(0,1,3)(0,0,0)[0]          
Hour 11:  ARIMA(1,0,3)(0,0,0)[0] intercept
Hour 12:  ARIMA(1,0,3)(0,0,0)[0] intercept
Hour 13:  ARIMA(2,0,2)(0,0,0)[0]          
Hour 14:  ARIMA(1,1,1)(0,0,0)[0]          
Hour 15:  ARIMA(1,1,1)(0,0,0)[0]          
Hour 16:  ARIMA(1,1,1)(0,0,0)[0]          
Hour 17:  ARIMA(3,1,4)(0,0,0)[0]          
Hour 18:  ARIMA(3,0,3)(0,0,0)[0]          
Hour 19:  ARIMA(0,0,0)(0,0,0)[0] intercept
Hour 20:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 21:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 22:  ARIMA(0,0,0)(0,0,0)[0]          
Hour 23:  ARIMA(0,0,0)(0,0,0)[0] 


```python
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
import numpy as np

# Initialize a dictionary to store the models for each hour
arima_models = {}

# Iterate through each hour of the day
for hour in range(24):
    # Filter data for the specific hour
    hourly_data = train_data[train_data['datetime'].dt.hour == hour]['production']
    
    # Build the ARIMA model using auto_arima
    model = auto_arima(hourly_data, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
    
    # Store the model in the dictionary
    arima_models[hour] = model

# Display the fitted models
print("Fitted ARIMA Models for Each Hour:")
for hour, model in arima_models.items():
    print(f"Hour {hour}: {model}")

```

    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    

     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16100.860, Time=0.12 sec
    Total fit time: 0.119 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16079.672, Time=0.05 sec
    Total fit time: 0.047 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16079.672, Time=0.05 sec
    Total fit time: 0.049 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16079.672, Time=0.05 sec
    Total fit time: 0.050 seconds
    Performing stepwise search to minimize aic
    

    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    

     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=-4716.791, Time=0.41 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=-4394.500, Time=0.13 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=-4623.541, Time=0.08 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=-4685.997, Time=0.13 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=-4396.500, Time=0.04 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=-4717.778, Time=0.34 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=-4721.478, Time=0.16 sec
     ARIMA(0,1,3)(0,0,0)[0] intercept   : AIC=-4739.694, Time=0.71 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=-4723.514, Time=0.48 sec
     ARIMA(0,1,4)(0,0,0)[0] intercept   : AIC=-4776.553, Time=0.98 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=-4841.333, Time=0.94 sec
     ARIMA(2,1,4)(0,0,0)[0] intercept   : AIC=-4879.947, Time=0.98 sec
     ARIMA(2,1,3)(0,0,0)[0] intercept   : AIC=-4780.332, Time=0.92 sec
     ARIMA(3,1,4)(0,0,0)[0] intercept   : AIC=-4869.645, Time=1.08 sec
     ARIMA(2,1,5)(0,0,0)[0] intercept   : AIC=-4868.954, Time=1.18 sec
     ARIMA(1,1,5)(0,0,0)[0] intercept   : AIC=-4846.131, Time=1.09 sec
     ARIMA(3,1,3)(0,0,0)[0] intercept   : AIC=-4847.057, Time=1.07 sec
     ARIMA(3,1,5)(0,0,0)[0] intercept   : AIC=-4877.792, Time=1.44 sec
     ARIMA(2,1,4)(0,0,0)[0]             : AIC=-4883.151, Time=0.60 sec
     ARIMA(1,1,4)(0,0,0)[0]             : AIC=-4842.211, Time=0.40 sec
     ARIMA(2,1,3)(0,0,0)[0]             : AIC=-4788.974, Time=0.49 sec
     ARIMA(3,1,4)(0,0,0)[0]             : AIC=-4877.811, Time=0.67 sec
     ARIMA(2,1,5)(0,0,0)[0]             : AIC=-4875.138, Time=0.68 sec
     ARIMA(1,1,3)(0,0,0)[0]             : AIC=-4725.519, Time=0.47 sec
     ARIMA(1,1,5)(0,0,0)[0]             : AIC=-4849.331, Time=0.59 sec
     ARIMA(3,1,3)(0,0,0)[0]             : AIC=-4849.245, Time=0.57 sec
     ARIMA(3,1,5)(0,0,0)[0]             : AIC=-4879.915, Time=0.84 sec
    
    Best model:  ARIMA(2,1,4)(0,0,0)[0]          
    Total fit time: 17.515 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=-1328.466, Time=0.73 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=-958.373, Time=0.08 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=-1189.321, Time=0.05 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=-1327.386, Time=0.15 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=-960.373, Time=0.04 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=-1324.745, Time=0.57 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=-1325.205, Time=0.39 sec
     ARIMA(3,1,2)(0,0,0)[0] intercept   : AIC=-1324.147, Time=0.85 sec
     ARIMA(2,1,3)(0,0,0)[0] intercept   : AIC=-1340.154, Time=0.97 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=-1327.484, Time=0.67 sec
     ARIMA(3,1,3)(0,0,0)[0] intercept   : AIC=-1333.521, Time=0.98 sec
     ARIMA(2,1,4)(0,0,0)[0] intercept   : AIC=-1333.543, Time=1.04 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=-1328.371, Time=0.85 sec
     ARIMA(3,1,4)(0,0,0)[0] intercept   : AIC=-1339.630, Time=1.31 sec
     ARIMA(2,1,3)(0,0,0)[0]             : AIC=-1361.576, Time=0.56 sec
     ARIMA(1,1,3)(0,0,0)[0]             : AIC=-1329.484, Time=0.33 sec
     ARIMA(2,1,2)(0,0,0)[0]             : AIC=-1330.711, Time=0.50 sec
     ARIMA(3,1,3)(0,0,0)[0]             : AIC=-1336.234, Time=0.58 sec
     ARIMA(2,1,4)(0,0,0)[0]             : AIC=inf, Time=0.73 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=-1326.745, Time=0.25 sec
     ARIMA(1,1,4)(0,0,0)[0]             : AIC=-1330.398, Time=0.37 sec
     ARIMA(3,1,2)(0,0,0)[0]             : AIC=-1332.835, Time=0.59 sec
     ARIMA(3,1,4)(0,0,0)[0]             : AIC=inf, Time=0.85 sec
    
    Best model:  ARIMA(2,1,3)(0,0,0)[0]          
    Total fit time: 13.427 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=1267.368, Time=0.65 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=1595.564, Time=0.06 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=1423.278, Time=0.06 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=1270.094, Time=0.10 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=1593.564, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=1270.978, Time=0.46 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=1270.931, Time=0.38 sec
     ARIMA(3,1,2)(0,0,0)[0] intercept   : AIC=1271.124, Time=0.73 sec
     ARIMA(2,1,3)(0,0,0)[0] intercept   : AIC=1250.329, Time=0.59 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=1267.378, Time=0.90 sec
     ARIMA(3,1,3)(0,0,0)[0] intercept   : AIC=1252.324, Time=1.08 sec
     ARIMA(2,1,4)(0,0,0)[0] intercept   : AIC=1252.323, Time=1.05 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=1270.112, Time=0.45 sec
     ARIMA(3,1,4)(0,0,0)[0] intercept   : AIC=1254.079, Time=1.14 sec
     ARIMA(2,1,3)(0,0,0)[0]             : AIC=1248.329, Time=0.32 sec
     ARIMA(1,1,3)(0,0,0)[0]             : AIC=1265.271, Time=0.41 sec
     ARIMA(2,1,2)(0,0,0)[0]             : AIC=1265.368, Time=0.35 sec
     ARIMA(3,1,3)(0,0,0)[0]             : AIC=1250.324, Time=0.63 sec
     ARIMA(2,1,4)(0,0,0)[0]             : AIC=1250.323, Time=0.57 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=1268.978, Time=0.17 sec
     ARIMA(1,1,4)(0,0,0)[0]             : AIC=1268.112, Time=0.23 sec
     ARIMA(3,1,2)(0,0,0)[0]             : AIC=1269.124, Time=0.21 sec
     ARIMA(3,1,4)(0,0,0)[0]             : AIC=1251.888, Time=0.70 sec
    
    Best model:  ARIMA(2,1,3)(0,0,0)[0]          
    Total fit time: 11.295 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=2743.121, Time=0.59 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3012.828, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=2872.736, Time=0.05 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=2771.521, Time=0.09 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3010.828, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=2747.744, Time=0.27 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=2746.436, Time=0.31 sec
     ARIMA(3,1,2)(0,0,0)[0] intercept   : AIC=2743.951, Time=0.83 sec
     ARIMA(2,1,3)(0,0,0)[0] intercept   : AIC=2744.215, Time=0.95 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=2748.161, Time=0.18 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=2745.992, Time=0.34 sec
     ARIMA(3,1,1)(0,0,0)[0] intercept   : AIC=2746.072, Time=0.25 sec
     ARIMA(3,1,3)(0,0,0)[0] intercept   : AIC=2742.352, Time=1.04 sec
     ARIMA(4,1,3)(0,0,0)[0] intercept   : AIC=inf, Time=1.18 sec
     ARIMA(3,1,4)(0,0,0)[0] intercept   : AIC=2747.516, Time=1.06 sec
     ARIMA(2,1,4)(0,0,0)[0] intercept   : AIC=2745.163, Time=1.11 sec
     ARIMA(4,1,2)(0,0,0)[0] intercept   : AIC=2745.238, Time=0.82 sec
     ARIMA(4,1,4)(0,0,0)[0] intercept   : AIC=2748.401, Time=1.42 sec
     ARIMA(3,1,3)(0,0,0)[0]             : AIC=inf, Time=0.83 sec
    
    Best model:  ARIMA(3,1,3)(0,0,0)[0] intercept
    Total fit time: 11.357 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=3331.561, Time=0.41 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3613.913, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=3468.974, Time=0.05 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=3361.209, Time=0.10 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3611.913, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=3331.114, Time=0.43 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=3341.204, Time=0.14 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=3333.898, Time=0.16 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=3330.628, Time=0.32 sec
     ARIMA(0,1,3)(0,0,0)[0] intercept   : AIC=3329.219, Time=0.21 sec
     ARIMA(0,1,4)(0,0,0)[0] intercept   : AIC=3330.315, Time=0.27 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=3330.080, Time=0.41 sec
     ARIMA(0,1,3)(0,0,0)[0]             : AIC=3327.219, Time=0.09 sec
     ARIMA(0,1,2)(0,0,0)[0]             : AIC=3339.204, Time=0.06 sec
     ARIMA(1,1,3)(0,0,0)[0]             : AIC=3328.628, Time=0.17 sec
     ARIMA(0,1,4)(0,0,0)[0]             : AIC=3328.316, Time=0.11 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=3329.115, Time=0.14 sec
     ARIMA(1,1,4)(0,0,0)[0]             : AIC=3328.080, Time=0.22 sec
    
    Best model:  ARIMA(0,1,3)(0,0,0)[0]          
    Total fit time: 3.318 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=3582.401, Time=0.58 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3863.351, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=3743.469, Time=0.07 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=3622.153, Time=0.11 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3861.351, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=3580.583, Time=0.33 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=3588.851, Time=0.16 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=3580.587, Time=0.17 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=3582.410, Time=0.49 sec
     ARIMA(0,1,3)(0,0,0)[0] intercept   : AIC=3580.992, Time=0.21 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=3580.454, Time=0.24 sec
     ARIMA(2,1,0)(0,0,0)[0] intercept   : AIC=3704.057, Time=0.11 sec
     ARIMA(3,1,1)(0,0,0)[0] intercept   : AIC=3582.401, Time=0.32 sec
     ARIMA(3,1,0)(0,0,0)[0] intercept   : AIC=3674.553, Time=0.12 sec
     ARIMA(3,1,2)(0,0,0)[0] intercept   : AIC=3584.415, Time=0.26 sec
     ARIMA(2,1,1)(0,0,0)[0]             : AIC=3578.456, Time=0.09 sec
     ARIMA(1,1,1)(0,0,0)[0]             : AIC=3578.588, Time=0.06 sec
     ARIMA(2,1,0)(0,0,0)[0]             : AIC=3702.057, Time=0.05 sec
     ARIMA(3,1,1)(0,0,0)[0]             : AIC=3580.403, Time=0.13 sec
     ARIMA(2,1,2)(0,0,0)[0]             : AIC=3580.403, Time=0.24 sec
     ARIMA(1,1,0)(0,0,0)[0]             : AIC=3741.469, Time=0.03 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=3578.586, Time=0.13 sec
     ARIMA(3,1,0)(0,0,0)[0]             : AIC=3672.554, Time=0.06 sec
     ARIMA(3,1,2)(0,0,0)[0]             : AIC=3582.412, Time=0.25 sec
    
    Best model:  ARIMA(2,1,1)(0,0,0)[0]          
    Total fit time: 4.266 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=3662.339, Time=0.55 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3960.203, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=3829.507, Time=0.07 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=3705.017, Time=0.10 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3958.203, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=3661.150, Time=0.30 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=3671.094, Time=0.18 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=3662.004, Time=0.19 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=3661.902, Time=0.51 sec
     ARIMA(0,1,3)(0,0,0)[0] intercept   : AIC=3660.785, Time=0.24 sec
     ARIMA(0,1,4)(0,0,0)[0] intercept   : AIC=3661.578, Time=0.32 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=3664.005, Time=0.46 sec
     ARIMA(0,1,3)(0,0,0)[0]             : AIC=3658.791, Time=0.10 sec
     ARIMA(0,1,2)(0,0,0)[0]             : AIC=3669.094, Time=0.07 sec
     ARIMA(1,1,3)(0,0,0)[0]             : AIC=3659.911, Time=0.22 sec
     ARIMA(0,1,4)(0,0,0)[0]             : AIC=3659.587, Time=0.13 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=3659.161, Time=0.12 sec
     ARIMA(1,1,4)(0,0,0)[0]             : AIC=3661.118, Time=0.41 sec
    
    Best model:  ARIMA(0,1,3)(0,0,0)[0]          
    Total fit time: 4.019 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,0,2)(0,0,0)[0]             : AIC=3646.719, Time=0.26 sec
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=5429.333, Time=0.01 sec
     ARIMA(1,0,0)(0,0,0)[0]             : AIC=3920.619, Time=0.02 sec
     ARIMA(0,0,1)(0,0,0)[0]             : AIC=4833.285, Time=0.05 sec
     ARIMA(1,0,2)(0,0,0)[0]             : AIC=3666.868, Time=0.16 sec
     ARIMA(2,0,1)(0,0,0)[0]             : AIC=3653.595, Time=0.21 sec
     ARIMA(3,0,2)(0,0,0)[0]             : AIC=3648.858, Time=0.52 sec
     ARIMA(2,0,3)(0,0,0)[0]             : AIC=3645.126, Time=0.34 sec
     ARIMA(1,0,3)(0,0,0)[0]             : AIC=3644.427, Time=0.21 sec
     ARIMA(0,0,3)(0,0,0)[0]             : AIC=4311.091, Time=0.10 sec
     ARIMA(1,0,4)(0,0,0)[0]             : AIC=3645.121, Time=0.43 sec
     ARIMA(0,0,2)(0,0,0)[0]             : AIC=4506.865, Time=0.07 sec
     ARIMA(0,0,4)(0,0,0)[0]             : AIC=4223.876, Time=0.15 sec
     ARIMA(2,0,4)(0,0,0)[0]             : AIC=3646.266, Time=0.67 sec
     ARIMA(1,0,3)(0,0,0)[0] intercept   : AIC=3640.856, Time=0.80 sec
     ARIMA(0,0,3)(0,0,0)[0] intercept   : AIC=3672.992, Time=0.15 sec
     ARIMA(1,0,2)(0,0,0)[0] intercept   : AIC=3655.663, Time=0.59 sec
     ARIMA(2,0,3)(0,0,0)[0] intercept   : AIC=3645.120, Time=0.88 sec
     ARIMA(1,0,4)(0,0,0)[0] intercept   : AIC=3641.941, Time=1.02 sec
     ARIMA(0,0,2)(0,0,0)[0] intercept   : AIC=3681.237, Time=0.12 sec
     ARIMA(0,0,4)(0,0,0)[0] intercept   : AIC=3673.221, Time=0.22 sec
     ARIMA(2,0,2)(0,0,0)[0] intercept   : AIC=3658.015, Time=0.40 sec
     ARIMA(2,0,4)(0,0,0)[0] intercept   : AIC=3644.649, Time=0.98 sec
    
    Best model:  ARIMA(1,0,3)(0,0,0)[0] intercept
    Total fit time: 8.364 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,0,2)(0,0,0)[0]             : AIC=3604.381, Time=0.26 sec
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=5407.406, Time=0.01 sec
     ARIMA(1,0,0)(0,0,0)[0]             : AIC=3897.516, Time=0.03 sec
     ARIMA(0,0,1)(0,0,0)[0]             : AIC=4806.947, Time=0.04 sec
     ARIMA(1,0,2)(0,0,0)[0]             : AIC=3610.715, Time=0.15 sec
     ARIMA(2,0,1)(0,0,0)[0]             : AIC=3605.301, Time=0.18 sec
     ARIMA(3,0,2)(0,0,0)[0]             : AIC=3606.729, Time=0.40 sec
     ARIMA(2,0,3)(0,0,0)[0]             : AIC=3606.073, Time=0.52 sec
     ARIMA(1,0,1)(0,0,0)[0]             : AIC=3633.313, Time=0.09 sec
     ARIMA(1,0,3)(0,0,0)[0]             : AIC=3604.173, Time=0.10 sec
     ARIMA(0,0,3)(0,0,0)[0]             : AIC=4310.969, Time=0.10 sec
     ARIMA(1,0,4)(0,0,0)[0]             : AIC=3606.104, Time=0.31 sec
     ARIMA(0,0,2)(0,0,0)[0]             : AIC=4479.616, Time=0.08 sec
     ARIMA(0,0,4)(0,0,0)[0]             : AIC=4211.827, Time=0.15 sec
     ARIMA(2,0,4)(0,0,0)[0]             : AIC=3607.536, Time=0.43 sec
     ARIMA(1,0,3)(0,0,0)[0] intercept   : AIC=3600.374, Time=0.76 sec
     ARIMA(0,0,3)(0,0,0)[0] intercept   : AIC=3652.132, Time=0.14 sec
     ARIMA(1,0,2)(0,0,0)[0] intercept   : AIC=3605.268, Time=0.61 sec
     ARIMA(2,0,3)(0,0,0)[0] intercept   : AIC=3606.688, Time=0.77 sec
     ARIMA(1,0,4)(0,0,0)[0] intercept   : AIC=3602.421, Time=0.90 sec
     ARIMA(0,0,2)(0,0,0)[0] intercept   : AIC=3658.417, Time=0.11 sec
     ARIMA(0,0,4)(0,0,0)[0] intercept   : AIC=3647.924, Time=0.21 sec
     ARIMA(2,0,2)(0,0,0)[0] intercept   : AIC=3606.284, Time=0.73 sec
     ARIMA(2,0,4)(0,0,0)[0] intercept   : AIC=3603.773, Time=0.99 sec
    
    Best model:  ARIMA(1,0,3)(0,0,0)[0] intercept
    Total fit time: 8.080 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,0,2)(0,0,0)[0]             : AIC=3701.639, Time=0.41 sec
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=5342.245, Time=0.01 sec
     ARIMA(1,0,0)(0,0,0)[0]             : AIC=3979.970, Time=0.03 sec
     ARIMA(0,0,1)(0,0,0)[0]             : AIC=4767.472, Time=0.04 sec
     ARIMA(1,0,2)(0,0,0)[0]             : AIC=3709.094, Time=0.14 sec
     ARIMA(2,0,1)(0,0,0)[0]             : AIC=3703.575, Time=0.19 sec
     ARIMA(3,0,2)(0,0,0)[0]             : AIC=inf, Time=0.57 sec
     ARIMA(2,0,3)(0,0,0)[0]             : AIC=3703.554, Time=0.38 sec
     ARIMA(1,0,1)(0,0,0)[0]             : AIC=3730.466, Time=0.09 sec
     ARIMA(1,0,3)(0,0,0)[0]             : AIC=3704.086, Time=0.21 sec
     ARIMA(3,0,1)(0,0,0)[0]             : AIC=3701.761, Time=0.25 sec
     ARIMA(3,0,3)(0,0,0)[0]             : AIC=3705.636, Time=0.55 sec
     ARIMA(2,0,2)(0,0,0)[0] intercept   : AIC=3708.568, Time=0.58 sec
    
    Best model:  ARIMA(2,0,2)(0,0,0)[0]          
    Total fit time: 3.446 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=inf, Time=0.57 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3873.114, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=3737.717, Time=0.05 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=3595.343, Time=0.09 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3871.114, Time=0.02 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=3572.753, Time=0.16 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=3573.436, Time=0.22 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=3573.227, Time=0.36 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=3575.728, Time=0.14 sec
     ARIMA(2,1,0)(0,0,0)[0] intercept   : AIC=3681.706, Time=0.09 sec
     ARIMA(1,1,1)(0,0,0)[0]             : AIC=3570.825, Time=0.07 sec
     ARIMA(0,1,1)(0,0,0)[0]             : AIC=3593.400, Time=0.03 sec
     ARIMA(1,1,0)(0,0,0)[0]             : AIC=3735.719, Time=0.03 sec
     ARIMA(2,1,1)(0,0,0)[0]             : AIC=3571.506, Time=0.09 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=3571.296, Time=0.17 sec
     ARIMA(0,1,2)(0,0,0)[0]             : AIC=3573.802, Time=0.06 sec
     ARIMA(2,1,0)(0,0,0)[0]             : AIC=3679.710, Time=0.04 sec
     ARIMA(2,1,2)(0,0,0)[0]             : AIC=inf, Time=0.31 sec
    
    Best model:  ARIMA(1,1,1)(0,0,0)[0]          
    Total fit time: 2.520 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=3236.260, Time=0.38 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3522.548, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=3387.793, Time=0.06 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=3254.049, Time=0.10 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3520.548, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=3234.816, Time=0.36 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=3236.518, Time=0.15 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=3233.561, Time=0.14 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=3234.589, Time=0.24 sec
     ARIMA(2,1,0)(0,0,0)[0] intercept   : AIC=3346.146, Time=0.07 sec
     ARIMA(1,1,1)(0,0,0)[0]             : AIC=3231.579, Time=0.06 sec
     ARIMA(0,1,1)(0,0,0)[0]             : AIC=3252.060, Time=0.04 sec
     ARIMA(1,1,0)(0,0,0)[0]             : AIC=3385.793, Time=0.03 sec
     ARIMA(2,1,1)(0,0,0)[0]             : AIC=3232.606, Time=0.10 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=3232.834, Time=0.16 sec
     ARIMA(0,1,2)(0,0,0)[0]             : AIC=3234.535, Time=0.06 sec
     ARIMA(2,1,0)(0,0,0)[0]             : AIC=3344.146, Time=0.03 sec
     ARIMA(2,1,2)(0,0,0)[0]             : AIC=3234.278, Time=0.18 sec
    
    Best model:  ARIMA(1,1,1)(0,0,0)[0]          
    Total fit time: 2.171 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=inf, Time=0.69 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=3002.033, Time=0.02 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=2883.832, Time=0.05 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=2760.143, Time=0.09 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=3000.033, Time=0.02 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=2737.902, Time=0.15 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=2739.740, Time=0.21 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=2739.729, Time=0.27 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=2740.117, Time=0.12 sec
     ARIMA(2,1,0)(0,0,0)[0] intercept   : AIC=2832.725, Time=0.07 sec
     ARIMA(1,1,1)(0,0,0)[0]             : AIC=2735.902, Time=0.06 sec
     ARIMA(0,1,1)(0,0,0)[0]             : AIC=2758.143, Time=0.10 sec
     ARIMA(1,1,0)(0,0,0)[0]             : AIC=2881.832, Time=0.03 sec
     ARIMA(2,1,1)(0,0,0)[0]             : AIC=2737.741, Time=0.09 sec
     ARIMA(1,1,2)(0,0,0)[0]             : AIC=2737.730, Time=0.12 sec
     ARIMA(0,1,2)(0,0,0)[0]             : AIC=2738.117, Time=0.06 sec
     ARIMA(2,1,0)(0,0,0)[0]             : AIC=2830.726, Time=0.04 sec
     ARIMA(2,1,2)(0,0,0)[0]             : AIC=inf, Time=0.47 sec
    
    Best model:  ARIMA(1,1,1)(0,0,0)[0]          
    Total fit time: 2.654 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=1800.794, Time=0.49 sec
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=2031.240, Time=0.07 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=1928.249, Time=0.05 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=1836.970, Time=0.15 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=2029.240, Time=0.02 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=1805.579, Time=0.30 sec
     ARIMA(2,1,1)(0,0,0)[0] intercept   : AIC=1805.537, Time=0.20 sec
     ARIMA(3,1,2)(0,0,0)[0] intercept   : AIC=1801.507, Time=0.58 sec
     ARIMA(2,1,3)(0,0,0)[0] intercept   : AIC=1782.818, Time=1.08 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=1806.902, Time=0.23 sec
     ARIMA(3,1,3)(0,0,0)[0] intercept   : AIC=1785.164, Time=1.20 sec
     ARIMA(2,1,4)(0,0,0)[0] intercept   : AIC=1781.511, Time=1.03 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=1799.406, Time=0.96 sec
     ARIMA(3,1,4)(0,0,0)[0] intercept   : AIC=1775.879, Time=1.08 sec
     ARIMA(4,1,4)(0,0,0)[0] intercept   : AIC=1779.848, Time=1.11 sec
     ARIMA(3,1,5)(0,0,0)[0] intercept   : AIC=1776.965, Time=1.25 sec
     ARIMA(2,1,5)(0,0,0)[0] intercept   : AIC=1783.933, Time=1.33 sec
     ARIMA(4,1,3)(0,0,0)[0] intercept   : AIC=1783.984, Time=1.21 sec
     ARIMA(4,1,5)(0,0,0)[0] intercept   : AIC=1779.233, Time=1.41 sec
     ARIMA(3,1,4)(0,0,0)[0]             : AIC=1773.734, Time=0.66 sec
     ARIMA(2,1,4)(0,0,0)[0]             : AIC=1779.034, Time=0.60 sec
     ARIMA(3,1,3)(0,0,0)[0]             : AIC=1778.857, Time=0.66 sec
     ARIMA(4,1,4)(0,0,0)[0]             : AIC=1777.723, Time=0.83 sec
     ARIMA(3,1,5)(0,0,0)[0]             : AIC=1774.945, Time=0.82 sec
     ARIMA(2,1,3)(0,0,0)[0]             : AIC=1780.818, Time=0.41 sec
     ARIMA(2,1,5)(0,0,0)[0]             : AIC=1781.933, Time=0.47 sec
     ARIMA(4,1,3)(0,0,0)[0]             : AIC=1781.978, Time=0.77 sec
     ARIMA(4,1,5)(0,0,0)[0]             : AIC=1777.237, Time=0.95 sec
    
    Best model:  ARIMA(3,1,4)(0,0,0)[0]          
    Total fit time: 19.944 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,0,2)(0,0,0)[0]             : AIC=214.010, Time=0.31 sec
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=421.563, Time=0.04 sec
     ARIMA(1,0,0)(0,0,0)[0]             : AIC=352.678, Time=0.03 sec
     ARIMA(0,0,1)(0,0,0)[0]             : AIC=376.947, Time=0.04 sec
     ARIMA(1,0,2)(0,0,0)[0]             : AIC=213.551, Time=0.24 sec
     ARIMA(0,0,2)(0,0,0)[0]             : AIC=340.017, Time=0.06 sec
     ARIMA(1,0,1)(0,0,0)[0]             : AIC=214.174, Time=0.13 sec
     ARIMA(1,0,3)(0,0,0)[0]             : AIC=215.547, Time=0.18 sec
     ARIMA(0,0,3)(0,0,0)[0]             : AIC=317.113, Time=0.10 sec
     ARIMA(2,0,1)(0,0,0)[0]             : AIC=213.553, Time=0.23 sec
     ARIMA(2,0,3)(0,0,0)[0]             : AIC=205.290, Time=0.34 sec
     ARIMA(3,0,3)(0,0,0)[0]             : AIC=198.590, Time=0.58 sec
     ARIMA(3,0,2)(0,0,0)[0]             : AIC=215.908, Time=0.47 sec
     ARIMA(4,0,3)(0,0,0)[0]             : AIC=208.836, Time=0.71 sec
     ARIMA(3,0,4)(0,0,0)[0]             : AIC=206.294, Time=0.68 sec
     ARIMA(2,0,4)(0,0,0)[0]             : AIC=206.529, Time=0.64 sec
     ARIMA(4,0,2)(0,0,0)[0]             : AIC=206.226, Time=0.56 sec
     ARIMA(4,0,4)(0,0,0)[0]             : AIC=inf, Time=1.21 sec
     ARIMA(3,0,3)(0,0,0)[0] intercept   : AIC=206.661, Time=0.94 sec
    
    Best model:  ARIMA(3,0,3)(0,0,0)[0]          
    Total fit time: 7.489 seconds
    Performing stepwise search to minimize aic
     ARIMA(2,0,2)(0,0,0)[0]             : AIC=-8051.975, Time=0.16 sec
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-8059.994, Time=0.04 sec
     ARIMA(1,0,0)(0,0,0)[0]             : AIC=-8057.994, Time=0.08 sec
     ARIMA(0,0,1)(0,0,0)[0]             : AIC=-8057.994, Time=0.08 sec
     ARIMA(1,0,1)(0,0,0)[0]             : AIC=-8055.994, Time=0.11 sec
     ARIMA(0,0,0)(0,0,0)[0] intercept   : AIC=-8060.270, Time=0.09 sec
     ARIMA(1,0,0)(0,0,0)[0] intercept   : AIC=-8058.277, Time=0.14 sec
     ARIMA(0,0,1)(0,0,0)[0] intercept   : AIC=-8058.276, Time=0.32 sec
     ARIMA(1,0,1)(0,0,0)[0] intercept   : AIC=-8056.276, Time=0.41 sec
    
    Best model:  ARIMA(0,0,0)(0,0,0)[0] intercept
    Total fit time: 1.437 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16100.860, Time=0.05 sec
    Total fit time: 0.049 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16100.860, Time=0.05 sec
    Total fit time: 0.049 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16100.860, Time=0.05 sec
    Total fit time: 0.048 seconds
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=-16100.860, Time=0.05 sec
    Total fit time: 0.048 seconds
    Fitted ARIMA Models for Each Hour:
    Hour 0:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 1:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 2:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 3:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 4:  ARIMA(2,1,4)(0,0,0)[0]          
    Hour 5:  ARIMA(2,1,3)(0,0,0)[0]          
    Hour 6:  ARIMA(2,1,3)(0,0,0)[0]          
    Hour 7:  ARIMA(3,1,3)(0,0,0)[0] intercept
    Hour 8:  ARIMA(0,1,3)(0,0,0)[0]          
    Hour 9:  ARIMA(2,1,1)(0,0,0)[0]          
    Hour 10:  ARIMA(0,1,3)(0,0,0)[0]          
    Hour 11:  ARIMA(1,0,3)(0,0,0)[0] intercept
    Hour 12:  ARIMA(1,0,3)(0,0,0)[0] intercept
    Hour 13:  ARIMA(2,0,2)(0,0,0)[0]          
    Hour 14:  ARIMA(1,1,1)(0,0,0)[0]          
    Hour 15:  ARIMA(1,1,1)(0,0,0)[0]          
    Hour 16:  ARIMA(1,1,1)(0,0,0)[0]          
    Hour 17:  ARIMA(3,1,4)(0,0,0)[0]          
    Hour 18:  ARIMA(3,0,3)(0,0,0)[0]          
    Hour 19:  ARIMA(0,0,0)(0,0,0)[0] intercept
    Hour 20:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 21:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 22:  ARIMA(0,0,0)(0,0,0)[0]          
    Hour 23:  ARIMA(0,0,0)(0,0,0)[0]          
    

    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\auto.py:444: UserWarning: Input time-series is completely constant; returning a (0, 0, 0) ARMA.
      warnings.warn('Input time-series is completely constant; '
    

Because of my computer I could not run this code very well, My point for this code is put the data into sarima because of seasonality 24 hour


```python
import numpy as np
from pmdarima import auto_arima

# Ensure no NaN or infinite values
train_data_cleaned = train_data.replace([np.inf, -np.inf], np.nan).dropna()

# Build the SARIMA model using auto_arima with more simplified parameters
sarima_model = auto_arima(
    train_data_cleaned['production'], 
    seasonal=True, 
    m=24,
    trace=True, 
    error_action='ignore', 
    suppress_warnings=True,
    start_p=1,  # Start value for p
    max_p=1,    # Further limit model complexity
    max_d=1, 
    start_q=0,  # Start value for q
    max_q=1, 
    start_P=0,  # Start value for seasonal P
    max_P=1, 
    max_D=1, 
    start_Q=0,  # Start value for seasonal Q
    max_Q=1,
    stepwise=True,      # Use stepwise search for better performance
    n_jobs=1            # Use a single CPU for memory efficiency
)

# Display the fitted SARIMA model
print("Fitted SARIMA Model:")
print(sarima_model.summary())

```

    Performing stepwise search to minimize aic
     ARIMA(1,1,0)(0,0,0)[24] intercept   : AIC=67531.524, Time=0.78 sec
     ARIMA(0,1,0)(0,0,0)[24] intercept   : AIC=69779.862, Time=0.29 sec
     ARIMA(1,1,0)(1,0,0)[24] intercept   : AIC=62171.907, Time=8.49 sec
     ARIMA(0,1,1)(0,0,1)[24] intercept   : AIC=65116.701, Time=6.82 sec
     ARIMA(0,1,0)(0,0,0)[24]             : AIC=69777.862, Time=0.25 sec
     ARIMA(1,1,0)(1,0,1)[24] intercept   : AIC=inf, Time=24.79 sec
     ARIMA(1,1,0)(0,0,1)[24] intercept   : AIC=65005.803, Time=7.07 sec
     ARIMA(0,1,0)(1,0,0)[24] intercept   : AIC=62231.302, Time=6.06 sec
     ARIMA(1,1,1)(1,0,0)[24] intercept   : AIC=inf, Time=62.66 sec
     ARIMA(0,1,1)(1,0,0)[24] intercept   : AIC=62170.158, Time=7.82 sec
     ARIMA(0,1,1)(0,0,0)[24] intercept   : AIC=68062.363, Time=1.06 sec
     ARIMA(0,1,1)(1,0,1)[24] intercept   : AIC=inf, Time=23.69 sec
     ARIMA(0,1,1)(1,0,0)[24]             : AIC=62168.158, Time=3.26 sec
     ARIMA(0,1,1)(0,0,0)[24]             : AIC=68060.363, Time=0.54 sec
     ARIMA(0,1,1)(1,0,1)[24]             : AIC=inf, Time=9.61 sec
     ARIMA(0,1,1)(0,0,1)[24]             : AIC=65114.701, Time=3.46 sec
     ARIMA(0,1,0)(1,0,0)[24]             : AIC=62229.302, Time=2.03 sec
     ARIMA(1,1,1)(1,0,0)[24]             : AIC=inf, Time=14.16 sec
     ARIMA(1,1,0)(1,0,0)[24]             : AIC=62169.907, Time=5.33 sec
    
    Best model:  ARIMA(0,1,1)(1,0,0)[24]          
    Total fit time: 188.247 seconds
    Fitted SARIMA Model:
                                          SARIMAX Results                                      
    ===========================================================================================
    Dep. Variable:                                   y   No. Observations:                18228
    Model:             SARIMAX(0, 1, 1)x(1, 0, [], 24)   Log Likelihood              -31081.079
    Date:                             Thu, 06 Jun 2024   AIC                          62168.158
    Time:                                     23:22:00   BIC                          62191.590
    Sample:                                          0   HQIC                         62175.859
                                               - 18228                                         
    Covariance Type:                               opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ma.L1         -0.0712      0.004    -16.990      0.000      -0.079      -0.063
    ar.S.L24       0.6137      0.003    177.861      0.000       0.607       0.620
    sigma2         1.7717      0.009    201.392      0.000       1.754       1.789
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.01   Jarque-Bera (JB):             49573.07
    Prob(Q):                              0.90   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.67   Skew:                            -0.06
    Prob(H) (two-sided):                  0.00   Kurtosis:                        11.08
    ===================================================================================
    
    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    

I tried it again but it is not working.


```python
from pmdarima import auto_arima

# Build the SARIMA model using auto_arima with limited search space and parallel processing
sarima_model = auto_arima(train_data['production'],
                          seasonal=True,
                          m=24,  # Adjust the seasonal period
                          start_p=0, max_p=1,  # Constrain AR orders
                          start_q=0, max_q=1,  # Constrain MA orders
                          start_P=0, max_P=1,  # Constrain seasonal AR orders
                          start_Q=0, max_Q=1,  # Constrain seasonal MA orders
                          d=1, D=1,  # Specify differences
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True,
                          n_jobs=4)  # Enable parallel processing with 4 cores

# Display the fitted SARIMA model
print("Fitted SARIMA Model:")
print(sarima_model)

```

    C:\Users\ardak\anaconda3\lib\site-packages\pmdarima\arima\_validation.py:76: UserWarning: stepwise model cannot be fit in parallel (n_jobs=1). Falling back to stepwise parameter search.
      warnings.warn('stepwise model cannot be fit in parallel (n_jobs=%i). '
    

    Performing stepwise search to minimize aic
     ARIMA(0,1,0)(0,1,0)[24]             : AIC=66419.063, Time=2.49 sec
     ARIMA(1,1,0)(1,1,0)[24]             : AIC=60996.127, Time=9.25 sec
     ARIMA(0,1,1)(0,1,1)[24]             : AIC=inf, Time=14.28 sec
     ARIMA(1,1,0)(0,1,0)[24]             : AIC=65745.125, Time=2.78 sec
     ARIMA(1,1,0)(1,1,1)[24]             : AIC=inf, Time=23.44 sec
     ARIMA(1,1,0)(0,1,1)[24]             : AIC=inf, Time=21.49 sec
     ARIMA(0,1,0)(1,1,0)[24]             : AIC=61559.660, Time=14.96 sec
    


```python
I put it into a lineer regression model also.
```


```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Check for NaN and infinite values in the dataset
print("Checking for NaN values:")
print(train_data.isna().sum())

print("\nChecking for infinite values:")
print(np.isinf(train_data).sum())

# Handle NaN and infinite values
# Option 1: Drop rows with NaN or infinite values
train_data_cleaned = train_data.replace([np.inf, -np.inf], np.nan).dropna()

# Option 2: Impute NaN and infinite values (for example, with the mean of the column)
# train_data_cleaned = train_data.replace([np.inf, -np.inf], np.nan)
# train_data_cleaned.fillna(train_data_cleaned.mean(), inplace=True)

# Extract features and target variable from the cleaned data
X_train = train_data_cleaned.drop(columns=['datetime', 'production'])
y_train = train_data_cleaned['production']

# Build the linear regression model
lin_reg_model = LinearRegression()
lin_reg_model.fit(X_train, y_train)

# Make predictions on the training data
train_preds = lin_reg_model.predict(X_train)

# Calculate residuals
train_residuals = y_train - train_preds

# Display the linear regression model coefficients and residuals
print("Linear Regression Model Coefficients:")
print(lin_reg_model.coef_)

print("\nTraining Residuals:")
print(train_residuals.head(10))

```


```python
I analyzed the residuals of ARIMA.
```


```python
# Build the ARIMA model on the residuals using auto_arima
residual_arima_model = auto_arima(train_residuals, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)

# Display the fitted ARIMA model on residuals
print("Fitted ARIMA Model on Residuals:")
print(residual_arima_model)

```

Because of my computer capabilitites I could not run this code. Lower MSE is the better model for this data.


```python
# Function to evaluate the models
def evaluate_model(model, test_data, hour=None):
    # If hour is specified, filter the test data for that hour
    if hour is not None:
        test_data = test_data[test_data['datetime'].dt.hour == hour]
    
    # Make predictions
    preds = model.predict(n_periods=len(test_data))
    
    # Calculate the mean squared error
    mse = mean_squared_error(test_data['production'], preds)
    
    return mse

# Evaluate ARIMA models for each hour
arima_mse = []
for hour, model in arima_models.items():
    mse = evaluate_model(model, test_data, hour)
    arima_mse.append(mse)

# Evaluate SARIMA model
sarima_mse = evaluate_model(sarima_model, test_data)

# Evaluate hybrid model
# Step 1: Make initial predictions using linear regression
X_test = test_data.drop(columns=['datetime', 'production'])
initial_preds = lin_reg_model.predict(X_test)

# Step 2: Predict residuals using ARIMA model
residual_preds = residual_arima_model.predict(n_periods=len(test_data))

# Step 3: Combine initial predictions and residual predictions
hybrid_preds = initial_preds + residual_preds

# Calculate the mean squared error for the hybrid model
hybrid_mse = mean_squared_error(test_data['production'], hybrid_preds)

# Display the mean squared errors for all models
print("\nMean Squared Errors:")
print(f"ARIMA Models (hourly): {np.mean(arima_mse)}")
print(f"SARIMA Model: {sarima_mse}")
print(f"Hybrid Model: {hybrid_mse}")

```


```python

```


```python

```
