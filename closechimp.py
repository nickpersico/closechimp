# Closechimp

from mailchimp_reader import recipients_by_campaign
from mailchimp_reader import recipient_activity
from mailchimp_reader import campaign_content
from mailchimp_reader import campaign_headers
from closeio import find_email_in_closeio
from closeio import send_email_to_closeio



# Step 1: Retrieve a list of campaigns and their recipients
recipients_by_campaign = recipients_by_campaign()

# Step 2: Identify what the recipient did within each campaign
for r in recipients_by_campaign:
	recipient_data = recipient_activity(r['campaign'], r['recipients'])
	print "campaign: %s, no of recipients: %d" % (r['campaign'], len(recipient_data))

	# Step 3: Grab the HTML from each campaign
	campaign_html = campaign_content(r['campaign'])

	# Step 4: Grab when the campaign was sent
	campaign_headers = campaign_headers(r['campaign'])

	# Step 5: Bring each email record together into a single sent email object for Close.io
	for ra in recipient_data:
		email = []

		email.append({
			"email": ra['email'],
			"from_name": campaign_headers[0]['from_name'],
			"from_email": campaign_headers[0]['from_email'],
			"subject": campaign_headers[0]['subject'],
			"date_sent": campaign_headers[0]['date_sent'],
			"html": campaign_html,
			"email_opens": ra['email_opens'],
			"latest_email_open": ra['latest_email_open']
		})
		# Step 6: Search for the contact email in Close.io
		contact_data = find_email_in_closeio(ra['email'])

		if contact_data != None:

			# Step 7: Send the email object to Close.io
			send_email_to_closeio(email, contact_data)

		print send_email_to_closeio
