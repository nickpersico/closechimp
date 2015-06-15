# Close.io Function File

from keys import closeio_key
from datetime import datetime
import requests0 as requests
import json
import urllib


def find_email_in_closeio(email):
	contact_data = []
	# Search for a contact's email in Close.io, return lead_id and contact_id
	email_query = "email:%s" % email
	query_url = 'https://app.close.io/api/v1/lead/?query=%s' % urllib.quote_plus(email_query)
	lead_data = requests.get(query_url, auth=(closeio_key, ''), headers={'Content-Type': 'application/json'})

	if lead_data.json['total_results'] == 0:
		return None
	lead = lead_data.json['data'][0]
	
	# Append necessary information from Close.io lead, unless there is no contact
	lead_id = lead['id']
	contacts = lead['contacts']

	unmatched_contact = True

	while unmatched_contact:
		for contact in contacts:
			for closeio_email in contact['emails']:
				if closeio_email['email'] == email:
					print "found emails -- %s" % email
					unmatched_contact = False

			if unmatched_contact == False:
				contact_id = contact['id']
				contact_data.append({"lead_id": lead_id, "contact_id": contact_id})
				return contact_data

			if unmatched_contact == True:
				return None
				

def send_email_to_closeio(email, contact_data):
	# Posts the email object to Close.io

	email_data = {
		"contact_id": contact_data[0]['contact_id'],
		"lead_id": contact_data[0]['lead_id'],
		"direction": "outgoing",
		"date_created": email[0]['date_sent'],
		"subject": email[0]['subject'],
		"sender": email[0]['from_email'],
		"to": [email[0]['email']],
		"status": "sent",
		"body_html": email[0]['html'],
	}
	email_url = 'https://app.close.io/api/v1/activity/email/'
	post_email = requests.post(email_url, auth=(closeio_key, ''), data=json.dumps(email_data), headers={'Content-Type': 'application/json'})
	
	return post_email.status_code
