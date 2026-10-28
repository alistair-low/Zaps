from datetime import datetime, time
from zoneinfo import ZoneInfo

today = datetime.now().astimezone(ZoneInfo('Europe/London'))

if today.time() < time(23,40):
    return []

return {'date': today.strftime('%Y-%m-%d'), 'pretty_date': today.strftime('%A, %-d %B %Y')}
