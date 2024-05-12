import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

#Load production data
production_df = pd.read_csv('production.csv')

# Load weather data
weather_df = pd.read_csv("weather_info.csv")

# Getting a template of dates and hours from the weather data
template_dt = weather_df[['date', 'hour']].drop_duplicates()
template_dt = pd.merge(template_dt, production_df, on=['date', 'hour'], how='left')
# Filter available data to include only hours between 21 and 4


# Ensure 'date' is a datetime type for comparison
template_dt['date'] = pd.to_datetime(template_dt['date'])

# Filter rows where date is less than or equal to tomorrow
template_dt = template_dt[template_dt['date'] <= pd.Timestamp('now').normalize() + pd.Timedelta(days=1)]

# Reshaping weather data for average computation
weather_melt = pd.melt(weather_df, id_vars=weather_df.columns[:4])

# Calculate hourly region averages
hourly_region_averages = weather_melt.groupby(['date', 'hour','variable'])['value'].mean().reset_index()

# Cast the long format data to wide format
hourly_region_averages_wide = hourly_region_averages.pivot_table(index=['date', 'hour'], columns='variable', values='value').reset_index()

# Reset the index to flatten the DataFrame after pivoting
hourly_region_averages_wide.reset_index(drop=True, inplace=True)

# Ensure 'date' is a datetime type for comparison
hourly_region_averages_wide['date'] = pd.to_datetime(hourly_region_averages_wide['date'])
# Merge with the template
template_dt_with_weather = pd.merge(template_dt, hourly_region_averages_wide, on=['date', 'hour'], how='left')
# Sort by date and hour
template_dt_with_weather.sort_values(by=['date', 'hour'], inplace=True)

# Separate data into available and to be forecasted
available_data = template_dt_with_weather[~template_dt_with_weather['production'].isna()]
to_be_forecasted = template_dt_with_weather[template_dt_with_weather['production'].isna()]


# Filter available data to include only hours between 5 AM and 9 PM
available_data = available_data[(available_data['hour'] >= 5) & (available_data['hour'] < 21)]
template_dt['date'] = pd.to_datetime(template_dt['date'])



available_data = available_data.dropna()
# Calculate correlation between weather variables and production for each location
correlation_results = {}
for location in available_data.columns[2:]:
    correlation_results[location] = available_data[['production', location]].corr().iloc[0, 1]

# Plot correlation results
plt.figure(figsize=(10, 6))
plt.bar(correlation_results.keys(), correlation_results.values(), color='skyblue')
plt.title('Correlation of Weather Variables with Production')
plt.xlabel('Location')
plt.ylabel('Correlation')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
# Veri setinde düzenli dönemsel desenleri gözlemlemek için haftalık ve aylık toplam üretim değerlerini inceleme
weekly_production = available_data.groupby(available_data['date'].dt.week)['production'].sum()
monthly_production = available_data.groupby(available_data['date'].dt.month)['production'].sum()

# Grafiklerin çizdirilmesi
plt.plot(weekly_production.index, weekly_production.values)
plt.xlabel('Week')
plt.ylabel('Production')
plt.title('Weekly Production')
plt.show()

plt.plot(monthly_production.index, monthly_production.values)
plt.xlabel('Month')
plt.ylabel('Production')
plt.title('Monthly Production')
plt.show()
# Take the difference of the production data twice with a lag of 24 hours each time
available_data['production_diff'] = available_data['production'].diff(periods=24)
to_be_forecasted['production_diff'] = to_be_forecasted['production'].diff(periods=24) 
# Drop NaN values resulting from differencing
available_data = available_data.dropna()
# Bağımsız ve bağımlı değişkenleri tanımlama
X = available_data.drop(columns=['date', 'hour', 'production_diff',"CSNOW_surface","TCDC_high.cloud.layer"])
y = available_data['production_diff']

# Modeli eğitme
lm_model2 = sm.OLS(y, sm.add_constant(X)).fit()

# Model özetini görüntüleme
print(lm_model2.summary())
import matplotlib.pyplot as plt
import seaborn as sns

# Modelin kalıntılarını hesapla
residuals = lm_model2.resid

# Kalıntıların histogramını çiz
plt.figure(figsize=(8, 6))
sns.histplot(residuals, kde=True)
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# QQ plot çiz
import statsmodels.api as sm
import scipy.stats as stats

fig = sm.qqplot(residuals, line ='45')
plt.title('QQ Plot of Residuals')
plt.show()
# ACF'nin çizimi
from statsmodels.graphics.tsaplots import plot_acf

# Kalıntıların ACF'sini çiz
plt.figure(figsize=(8, 6))
plot_acf(residuals, lags=20)  # 20 adet gecikme için ACF
plt.title('ACF of Residuals')
plt.xlabel('Lag')
plt.ylabel('ACF')
plt.show()
# Lag1 sütunu oluşturma
available_data['lag1'] = available_data['production_diff'].shift(1)
to_be_forecasted['lag1'] = to_be_forecasted['production_diff'].shift(1)
# Eksik değerleri temizleme
available_data.dropna(inplace=True)

# Bağımsız ve bağımlı değişkenleri tanımlama
X = available_data.drop(columns=['date', 'hour', "production",'production_diff',"TCDC_high.cloud.layer"])
y = available_data['production_diff']

# Modeli eğitme
lm_model = sm.OLS(y, sm.add_constant(X)).fit()

# Model özetini görüntüleme
print(lm_model.summary())
import matplotlib.pyplot as plt
import seaborn as sns

# Modelin kalıntılarını hesapla
residuals = lm_model.resid

# Kalıntıların histogramını çiz
plt.figure(figsize=(8, 6))
sns.histplot(residuals, kde=True)
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# QQ plot çiz
import statsmodels.api as sm
import scipy.stats as stats

fig = sm.qqplot(residuals, line ='45')
plt.title('QQ Plot of Residuals')
plt.show()
# ACF'nin çizimi
from statsmodels.graphics.tsaplots import plot_acf

# Kalıntıların ACF'sini çiz
plt.figure(figsize=(8, 6))
plot_acf(residuals, lags=20)  # 20 adet gecikme için ACF
plt.title('ACF of Residuals')
plt.xlabel('Lag')
plt.ylabel('ACF')
plt.show()
 Lag16 sütunu oluşturma
available_data['lag16'] = available_data['production_diff'].shift(16)
to_be_forecasted['lag16'] = to_be_forecasted['production_diff'].shift(16)
# Eksik değerleri temizleme
available_data.dropna(inplace=True)

# Bağımsız ve bağımlı değişkenleri tanımlama
X = available_data.drop(columns=['date', 'hour', 'production_diff',"production","TCDC_high.cloud.layer"])
y = available_data['production_diff']

# Modeli eğitme
lm_model3 = sm.OLS(y, sm.add_constant(X)).fit()

# Model özetini görüntüleme
print(lm_model3.summary())
import matplotlib.pyplot as plt
import seaborn as sns

# Modelin kalıntılarını hesapla
residuals = lm_model3.resid

# Kalıntıların histogramını çiz
plt.figure(figsize=(8, 6))
sns.histplot(residuals, kde=True)
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# QQ plot çiz
import statsmodels.api as sm
import scipy.stats as stats

fig = sm.qqplot(residuals, line ='45')
plt.title('QQ Plot of Residuals')
plt.show()
# ACF'nin çizimi
from statsmodels.graphics.tsaplots import plot_acf

# Kalıntıların ACF'sini çiz
plt.figure(figsize=(8, 6))
plot_acf(residuals, lags=20)  # 20 adet gecikme için ACF
plt.title('ACF of Residuals')
plt.xlabel('Lag')
plt.ylabel('ACF')
plt.show()
import pandas as pd
import statsmodels.api as sm

# Assuming 'to_be_forecasted' is your DataFrame
# Drop unnecessary columns
X_to_be_forecasted = to_be_forecasted.drop(columns=['date', 'hour', 'production_diff', "production", "TCDC_high.cloud.layer"])

# Check for missing values
missing_values = X_to_be_forecasted.isnull().sum()

# Handle missing values if any
# For example, you can impute missing values with mean
X_to_be_forecasted.fillna(0, inplace=True)

# Add constant to independent variables
X_to_be_forecasted = sm.add_constant(X_to_be_forecasted)

# Assuming 'lm_model3' is your trained model
# Check model parameters

# Predict production_diff using the trained model
predictions = lm_model3.predict(X_to_be_forecasted)

# Assign predictions back to the DataFrame using .loc after creating a copy
# Create a copy of the DataFrame
to_be_forecasted_copy = to_be_forecasted.copy()

# Assign predictions to the copy
to_be_forecasted_copy['production_diff_prediction'] = predictions

# Display the DataFrame with predictions
print(predictions)
from statsmodels.tsa.stattools import kpss

# Extract the production data
production_data = available_data['production_diff']

# Perform KPSS test
kpss_stat, p_value, lags, critical_values = kpss(production_data)

# Print the test results
print(f'KPSS Statistic: {kpss_stat}')
print(f'p-value: {p_value}')
print('Critical Values:')
for key, value in critical_values.items():
    print(f'   {key}: {value}')

# Interpret the results
if p_value < 0.05:
    print('Reject the null hypothesis (non-stationary).')
else:
    print('Fail to reject the null hypothesis (stationary).')
    
# Veri setinde düzenli dönemsel desenleri gözlemlemek için haftalık ve aylık toplam üretim değerlerini inceleme
weekly_production = available_data.groupby(available_data['date'].dt.week)['production'].sum()
monthly_production = available_data.groupby(available_data['date'].dt.month)['production'].sum()

# Grafiklerin çizdirilmesi
plt.plot(weekly_production.index, weekly_production.values)
plt.xlabel('Week')
plt.ylabel('Production')
plt.title('Weekly Production')
plt.show()

plt.plot(monthly_production.index, monthly_production.values)
plt.xlabel('Month')
plt.ylabel('Production')
plt.title('Monthly Production')
plt.show()
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# ACF ve PACF grafiklerini çizin
plot_acf(available_data['production_diff'], lags=50)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Function (ACF)')
plt.show()

plot_pacf(available_data['production_diff'], lags=50)
plt.xlabel('Lag')
plt.ylabel('Partial Autocorrelation')
plt.title('Partial Autocorrelation Function (PACF)')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# R'den alınan örnek veri
# template_dt_with_weather verisini yerine kendi veri çerçevenizi kullanmalısınız

# Tarih sütununu tarih nesnelerine dönüştürme
available_data['date'] = pd.to_datetime(available_data['date'])

# Tarih sütununu indeks yapma
available_data.set_index('date', inplace=True)

# Günlük veriye dönüştürme
daily_data = available_data.resample('D').agg({'production': ['sum', 'max', 'mean']})

# Sütun isimlerini düzenleme
daily_data.columns = ['total_p', 'max_p', 'mean_p']

# Grafik oluşturma
plt.figure(figsize=(10, 6))
plt.plot(daily_data.index, daily_data['total_p'], color='darkred')
plt.title('Daily Total Production for Available Data')
plt.xlabel('Date')
plt.ylabel('Production (MWh)')
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d %b %y'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
import matplotlib.pyplot as plt
import pandas as pd

# R'den alınan örnek veri
# daily_data verisini yerine kendi veri çerçevenizi kullanmalısınız

# Grafik oluşturma
plt.figure(figsize=(10, 6))
plt.plot(daily_data.index, daily_data['max_p'], color='darkred')
plt.title('Daily Maximum Production for Available Data')
plt.xlabel('Date')
plt.ylabel('Production (MWh)')
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d %b %y'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# Mevsimsel etkiyi çıkarıp görselleştirmek için bir fonksiyon tanımlayalım
def decompose_and_visualize(data, column_name):
    # Veri çerçevesinin indeksini tarih formatına dönüştürme
    data.index = pd.to_datetime(data.index)
    
    # Mevsimsel etkiyi çıkarma
    decomposed = seasonal_decompose(data[column_name], period=24)
    
    # Ayrıştırılmış veriyi görselleştirme
    plt.figure(figsize=(10, 8))
    plt.subplot(411)
    plt.plot(decomposed.observed, label='Observed')
    plt.legend(loc='upper left')
    plt.subplot(412)
    plt.plot(decomposed.trend, label='Trend')
    plt.legend(loc='upper left')
    plt.subplot(413)
    plt.plot(decomposed.seasonal, label='Seasonality')
    plt.legend(loc='upper left')
    plt.subplot(414)
    plt.plot(decomposed.resid, label='Random')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

# Fonksiyonu kullanarak mevsimsel etkiyi çıkarıp görselleştirelim
decompose_and_visualize(daily_data, 'mean_p')
# Calculate variance of the production data
variance = available_data['production_diff'].mean()

# Plotting
plt.figure(figsize=(20, 6))
plt.plot(available_data.index, available_data['production_diff'], label='Production')
plt.title('Production Variance')
plt.xlabel('Date')
plt.ylabel('Production')
plt.axhline(y=variance, color='r', linestyle='--', label='Variance')
plt.legend()
plt.show()