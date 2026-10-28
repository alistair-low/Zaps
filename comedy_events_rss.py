import requests
import urllib.parse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

today = datetime.now().astimezone(ZoneInfo('Europe/London'))

if today.time() < time(23,40):
    return []

last_run = today - timedelta(days=1)

ACCESS_TOKEN = '__TOKEN__'
PARAMS = {
    'lat': '55.92459',
    'lon': '-3.54490',
    'distance': '36',
    'tags': 'comedy,!film',
    'since': last_run.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
    'max_date': '3000-01-01T00:00:00.000Z',
}

next_page = 'https://api.datathistle.com/v1/events?' + urllib.parse.urlencode(PARAMS)
events = []

while next_page:
    response = requests.get(next_page, headers={'Authorization': f'Bearer {ACCESS_TOKEN}',})
    if response.status_code != 200:
        response.raise_for_status()
    events.extend(response.json())
    next_page = response.headers.get('X-Next', '')

transformed_events = []

for item in events:
    
    for schedule in item["schedules"]:
        event = {
            'name': f'{item["name"]} [{schedule["place"]["town"]}]',
            'description': ''
        }

        if schedule.get('performances'):
            performance = schedule['performances'][0]
            event['description'] += datetime.fromisoformat(performance['ts']).strftime('%A, %d %B %Y, %H:%M').replace('  ', ' ')
            if performance.get('links'):
                event['link'] = performance['links'][0]['url']

        if item.get('descriptions'):
            event['description'] += '\n\n' + item['descriptions'][0]['description']

        if item.get('images'):
            event['image'] = item['images'][0]['url']
        
        transformed_events.append(event)

return transformed_events
