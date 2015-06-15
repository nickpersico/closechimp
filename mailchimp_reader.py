# MailChimp List and Campaign Reader

from postmonkey import PostMonkey
from postmonkey import MailChimpException
from keys import mc_key
from keys import closeio_key
from datetime import datetime

chimp = PostMonkey(mc_key)


def recipients_by_campaign():
	# Retrieves a list of recipients by sent campaign
	recipients_by_campaign = []
	campaigns = chimp.campaigns(filters=[{'status': 'sent'}])
	campaign_ids = []

	for c in campaigns['data']:
		campaign_ids.append({"id": c['id'], "status": c['status']})

	for cid in campaign_ids:
		cm_member_emails = []

		if cid['status'] == 'sent':
			campaignmembers = chimp.campaignMembers(cid=cid['id'])

			for cm in campaignmembers['data']:
				cm_member_emails.append(cm['email'])

			recipients_by_campaign.append({"campaign": cid['id'], "recipients": cm_member_emails})

	return recipients_by_campaign


def recipient_activity(campaign, recipients):
	recipient_activity = []

	for recipient in recipients:
		recipient_data = chimp.campaignEmailStatsAIM(cid=campaign, email_address=recipient)
		email_opens = recipient_data['data'][0]['activity']
		
		open_data = []

		if len(email_opens) != 0:
			for eo in email_opens:
				open_data.append(eo['timestamp'])
			latest_email_open = min(open_data)
		else:
			latest_email_open = None

		recipient_activity.append({
			"campaign_id": campaign,
			"email": recipient,
			"email_opens": len(email_opens),
			"latest_email_open": latest_email_open
		})

		del open_data

	return recipient_activity

def campaign_content(campaign):
	content = chimp.campaignContent(cid=campaign)

	return content['html']

def campaign_headers(campaign):
	campaign_headers = []
	c_data = chimp.campaigns()
	
	for cp in c_data['data']:
		if cp['id'] == campaign:
			date_sent = cp['send_time']
			from_name = cp['from_name']
			from_email = cp['from_email']
			subject = cp['subject']

			campaign_headers.append({
				"date_sent": date_sent,
				"from_name": from_name,
				"from_email": from_email,
				"subject": subject
			})

	return campaign_headers
	



