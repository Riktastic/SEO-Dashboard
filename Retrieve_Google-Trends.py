# ### Libraries:
# Voor het uitvoeren van shell commando's:
from pytrends.request import TrendReq

# ### Instellingen:

#pytrends = TrendReq(hl='en-US', tz=360)
#print(pytrends)

kw_list = ["OneSquad", "Test"]

pytrends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)