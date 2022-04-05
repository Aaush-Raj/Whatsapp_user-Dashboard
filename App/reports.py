import pytz
from datetime import datetime, timedelta
from New import client


whatsapp = client.whatsapp
users = whatsapp.users
contacts = whatsapp.contacts
daily_updates = whatsapp.daily_updates
tender_access_logs = whatsapp.tender_access_logs


def get_reports():
    report = {}
    start_time_today = datetime.now(pytz.timezone(
        'Asia/Kolkata')).replace(hour=0, minute=0, second=0, microsecond=0)
    days_range = [0, 6, 13, 29]

    # Total users
    total_users = users.distinct('_id')
    total_count = len(total_users)

    # Counts
    active_users = []  # today, last 7 days, last 14 days, last 30 days
    onboarded_users = []  # today, last 7 days, last 14 days, last 30 days
    responded_to_daily_update = []  # today, last 7 days, last 14 days, last 30 days
    tender_accessed_users = []  # today, last 7 days, last 14 days, last 30 days
    tender_doc_accessed_users = []  # today, last 7 days, last 14 days, last 30 days

    for i in days_range:
        start_time = start_time_today - timedelta(days=i)
        active_users.append([x['_id'] for x in users.aggregate([
            {'$lookup': {
                'from': 'contacts',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'contact'
            }},
            {'$unwind': '$contact'},
            {'$match': {
                'contact.last_messaged_on': {'$gte': start_time}
            }},
            {'$project': {'_id': 1}}
        ])])

        onboarded_users.append(users.distinct(
            '_id', {'created_on': {'$gte': start_time}}))

        responded_to_daily_update.append(
            daily_updates.distinct(
                'wa_id', {'responses.timestamp': {'$gte': start_time}})
        )

        tender_accessed_users.append(tender_access_logs.distinct(
            'wa_id', {'timestamp': {'$gte': start_time}}))

        tender_doc_accessed_users.append(tender_access_logs.distinct(
            'wa_id', {'document_access_timestamp': {'$gte': start_time}}))

    active_users_count = [len(x) for x in active_users]
    onboarded_users_count = [len(x) for x in onboarded_users]
    responded_to_daily_update_count = [
        len(x) for x in responded_to_daily_update]
    tender_accessed_users_count = [len(x) for x in tender_accessed_users]
    tender_doc_accessed_users_count = [
        len(x) for x in tender_doc_accessed_users]

    todays_date = datetime.now(pytz.timezone(
        'Asia/Kolkata')).strftime('%d %B, %Y')

    active_inactive_count = [active_users_count[0],
                             total_count - active_users_count[0]]

    report.update({
        'total_users': total_count,
        'active_users': active_users_count,
        'active_inactive_count': active_inactive_count,
        'onboarded_users': onboarded_users_count,
        'responded_to_daily_update': responded_to_daily_update_count,
        'tender_accessed_users': tender_accessed_users_count,
        'tender_doc_accessed_users': tender_doc_accessed_users_count,
        'todays_date': todays_date
    })

    return report
