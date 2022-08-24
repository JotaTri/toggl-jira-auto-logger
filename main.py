import logging
import urllib
from datetime import datetime, timedelta

from jira import JIRA
from toggl.TogglPy import Toggl


TIME_DELTA = 7
TOGGL_API_TOKEN = ${{ secrets.TOGGL_API_TOKEN }}

JIRA_SERVER = ${{ secrets.JIRA_SERVER }}
JIRA_MAIL = ${{ secrets.JIRA_MAIL }}
JIRA_API_TOKEN = ${{ secrets.JIRA_API_TOKEN }}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

toggl_datetime_format = '%Y-%m-%dT%H:%M:%S+00:00'

start_date = datetime.strftime(datetime.now() - timedelta(days=TIME_DELTA), toggl_datetime_format)
end_date = datetime.strftime(datetime.now(), toggl_datetime_format)

logger.info('Authenticating on JIRA...')
jira = JIRA(server=JIRA_SERVER,
            basic_auth=(JIRA_MAIL, JIRA_API_TOKEN))
logger.info('Successfully authenticated on JIRA')

logger.info('Authenticating on Toggl...')
toggl: Toggl = Toggl()
toggl.setAPIKey(TOGGL_API_TOKEN)
logger.info('Successfully authenticated on Toggl')

logger.info(f'Getting Toggl`s entries of last {TIME_DELTA} days({start_date} - {end_date})')
try:
    query_params = f'start_date={urllib.parse.quote(start_date)}&end_date={urllib.parse.quote(end_date)}'
    response = toggl.request(f"https://api.track.toggl.com/api/v8/time_entries?{query_params}")
except Exception as e:
    logger.error(e)
    SystemExit()

logger.info(f'{len(response)} log entries located on defined time range')
logged_entries = 0
for entry in response:
    if 'tags' not in entry or 'logged' not in entry['tags']:
        try:
            logger.info(
                f'Adding worklog on issue {entry["description"]}' +
                f' of {float(entry["duration"])/3600:.2f}h on {entry["start"]}'
            )
            jira.add_worklog(
                entry['description'],
                timeSpentSeconds=str(entry['duration']),
                started=datetime.strptime(entry['start'], toggl_datetime_format)
            )
            logger.info('Sucessfull\n')
            logger.info('Adding "logged" tag on Toggl entry')
            if 'tags' in entry:
                entry['tags'].append('logged')
            else:
                entry['tags'] = ['logged']
            data = {"time_entry": entry}
            new_r = toggl.postRequest(
                f'https://api.track.toggl.com/api/v8/time_entries/{entry["id"]}',
                parameters=data, method='PUT'
            )
            logger.info('Sucessfull\n')
            logged_entries += 1
        except Exception as e:
            logger.error(f'Error on {entry["description"]} of {float(entry["duration"])/3600:.2f}h on {entry["start"]}')
            logger.error(e)

logger.info(f'Logged hours on JIRA of {logged_entries} entries')
logger.info('Ending Auto-logger execution')
