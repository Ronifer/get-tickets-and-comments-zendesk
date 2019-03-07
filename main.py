import requests
import json
import csv

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


def getComments(id_ticket):
    commentsToWrite = []
    commentsToWrite.append(str(id_ticket))
    credentials = '<ZENDESK LOGIN>', '<ZENDESK PASS>'
    session = requests.Session()
    session.auth = credentials
    url = "<ZENDESK PASS>/api/v2/tickets/"+str(id_ticket)+"/comments"
    response = session.get(url)
    if response.status_code != 200:
        print('Error with status code {}'.format(response.status_code))
        exit()
    data = response.json()
    for comment in data['comments']:
        commentsToWrite.append(comment['plain_body'])
    return commentsToWrite


credentials = '<ZENDESK LOGIN>', '<ZENDESK PASS>'
session = requests.Session()
session.auth = credentials
zendesk = '<ZENDESK URL>'

topic_id = 123456
topic_posts = []
url = zendesk + '/api/v2/search.json?query=type:ticket updated>"2018-05-01" updated<"2019-03-01"&sort_by=created_at'
with open('tickets.csv', mode='w') as ticket_file:
    ticket_writer = csv.writer(ticket_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open('comments.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        while url:
            response = session.get(url)
            if response.status_code != 200:
                print('Error with status code {}'.format(response.status_code))
                exit()
            data = response.json()
            
            for ticket in data['results']:
                ticketsToWrite = []
                print(ticket['id'])
                ticketsToWrite.append(ticket['id'])
                ticketsToWrite.append(ticket['created_at'])
                ticketsToWrite.append(ticket['updated_at'])
                ticketsToWrite.append(ticket['type'])
                ticketsToWrite.append(ticket['subject'])
                ticketsToWrite.append(ticket['raw_subject'])
                ticketsToWrite.append(ticket['description'])
                ticketsToWrite.append(ticket['status'])
                
                ticket_writer.writerow(ticketsToWrite)
                # GET COMMENTS
                employee_writer.writerow(getComments(ticket['id']))
            print(data['next_page'])
            url = data['next_page']
