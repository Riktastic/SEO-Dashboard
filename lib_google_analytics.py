"""Hello Analytics Reporting API V4."""

import argparse
import json
import sys

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
CLIENT_SECRETS_PATH = 'client_secret_43268433419-4s01b5323vlbujap349a9nl2dqmqnqu2.apps.googleusercontent.com.json' # Path to client_secrets.json file.
VIEW_ID = '208391169'


def ga_initialize():
  """Initializes the analyticsreporting service object.

  Returns:
    analytics an authorized analyticsreporting service object.
  """
  # Parse command-line arguments.
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])

  # Set up a Flow object to be used if we need to authenticate.
  flow = client.flow_from_clientsecrets(
      CLIENT_SECRETS_PATH, scope=SCOPES,
      message=tools.message_if_missing(CLIENT_SECRETS_PATH))

  # Prepare credentials, and authorize HTTP object with them.
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to a file.
  storage = file.Storage('analyticsreporting.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', http=http)

  return analytics

def ga_get_report_site(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'dimensions': [{'name': 'ga:dateHourMinute'}],         
          'metrics': [{'expression': 'ga:users'}, {'expression': 'ga:newUsers'}, {'expression': 'ga:sessions'}, {'expression': 'ga:sessionsPerUser'}, {'expression': 'ga:sessionDuration'}, {'expression': 'ga:avgSessionDuration'}, {'expression': 'ga:pageviews'}, {'expression': 'ga:pageviewsPerSession'}, {'expression': 'ga:entrances'}, {'expression': 'ga:organicSearches'}]
        }]
      }
  ).execute()
    
def ga_get_report_pages(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'dimensions': [{'name': 'ga:dateHourMinute'}, {'name': 'ga:pagePath'}, {'name': 'ga:pageTitle'}],         
          'metrics': [{'expression': 'ga:pageviews'}, {'expression': 'ga:avgTimeOnPage'}, {'expression': 'ga:avgPageLoadTime'}]
        }]
      }
  ).execute()

def ga_get_report_users_age(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'dimensions': [{'name': 'ga:dateHourMinute'}, {'name': 'ga:userAgeBracket'}],         
          'metrics': [{'expression': 'ga:users'}]
        }]
      }
  ).execute()

def ga_get_report_users_country(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'dimensions': [{'name': 'ga:dateHourMinute'}, {'name': 'ga:country'}, {'name': 'ga:countryIsoCode'}],
          'metrics': [{'expression': 'ga:users'}]
        }]
      }
  ).execute()

def ga_get_report_users_gender(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'dimensions': [{'name': 'ga:dateHourMinute'}, {'name': 'ga:userGender'}],         
          'metrics': [{'expression': 'ga:users'}]
        }]
      }
  ).execute()

def ga_convert_response_to_dict(response):
    columnheaders_dimensions = response['reports'][0]['columnHeader']['dimensions']
    columnheaders_metrics = response['reports'][0]['columnHeader']['metricHeader']['metricHeaderEntries']
    columnheaders = []
    output = []
    
    for i in columnheaders_dimensions:
        column = str(i).replace('ga:', '')
        columnheaders.append(column)
        
    for i in columnheaders_metrics:
        column = str(i['name']).replace('ga:', '')
        columnheaders.append(column)
    
    try:
        for i in response['reports'][0]['data']['rows']:
            values_dimensions = i['dimensions']
            values_metrics = i['metrics'][0]['values']
            values = []
    
            for x in values_dimensions:
                values.append(x)

            for y in values_metrics:
                values.append(y)
    
            converted = {columnheaders[i]: values[i] for i in range(0, len(columnheaders))} 
            output.append(converted)

    except KeyError:
        print("! Error, er zijn geen waarden meegeleverd aan dit response, probeer de query aan te passen of te wachten tot de data aanwezig is.")
        output = False

    return output
    

def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response"""

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range (' + str(i) + ')')
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ': ' + value)

def main():

  analytics = initialize_analyticsreporting()
  
  print("\nga_site:")
  print_response(get_report_site(analytics))

  print("\nga_pages:")
  print_response(get_report_pages(analytics))
  
  print("\nga_users_age:")
  print_response(get_report_users_age(analytics))
  
  print("\nga_users_country:")
  print_response(get_report_users_country(analytics))

  print("\nga_users_gender:")
  print_response(get_report_users_gender(analytics))
if __name__ == '__main__':
  main()
