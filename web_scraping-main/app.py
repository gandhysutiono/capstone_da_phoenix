from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table',attrs={'class':'table table-striped text-sm text-lg-normal'})
temp = soup.find_all('th',attrs={'class':'font-semibold text-center'})

row_length = len(temp)

temp = [] #initiating a list 

for i in range(0, row_length):
    # get period
    period = soup.find_all('th',attrs={'class':'font-semibold text-center'})[i].text
    period = period.strip('\n')
    
    # get Market Cap
    MarketCap = soup.find_all('td',attrs={'class':'text-center'})[i*4].text
    MarketCap = MarketCap.strip('\n')
    
    # get Volume
    Volume = soup.find_all('td',attrs={'class':'text-center'})[i*4+1].text
    Volume = Volume.strip('\n')
    
    # get Open
    Open = soup.find_all('td',attrs={'class':'text-center'})[i*4+2].text
    Open = Open.strip('\n')
    
    # get Close
    Close = soup.find_all('td',attrs={'class':'text-center'})[i*4+3].text
    Close = Close.strip('\n')
    
    #scrapping process
    temp.append((period,MarketCap,Volume,Open,Close))
    
temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp,columns = ('period','MarketCap','Volume','Open','Close'))

#insert data wrangling here

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)