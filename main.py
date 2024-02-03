import requests,config,smtplib

STOCK_NAME = "GOOG"
COMPANY_NAME = "Alphabet Inc Class C"

STOCK_ENDPOINT = config.stock_endpoint
MAIL = config.mail
STOCKS_API_KEY = config.stocks_api_key
PASS = config.password

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCKS_API_KEY
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_lst = [value for (key, value) in data.items()]
yesterday_data = data_lst[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print("Yesterday Closing Price: ",yesterday_closing_price)

day_before_yesterday_data = data_lst[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
print("Day Before Yesterday Closing Price: ",day_before_yesterday_closing_price)

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
print("Difference:",difference)

diff_percent = (difference / yesterday_closing_price) * 100
print("Difference Percentage:",round(diff_percent,3),"%")

if diff_percent > 1:
    mail = smtplib.SMTP("smtp.gmail.com")
    mail.starttls()
    mail.login(MAIL,PASS)
    mail.sendmail(MAIL,MAIL,
                  "subject: Stock Alert\n\nStock Name: "+STOCK_NAME+"\nCompany Name: "
                  +COMPANY_NAME+"\nDifference Percentage: "+str(round(diff_percent,3))+
                  "%\nDifference: "+str(difference))
    mail.quit()