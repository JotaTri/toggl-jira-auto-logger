import logging
import urllib
from datetime import datetime, timedelta
from openpyxl import Workbook, load_workbook
import sys
import traceback

from toggl.TogglPy import Toggl


# TIME_DELTA = 30
MONTH = 10
TOGGL_API_TOKEN = "132b838672207be5069f2b7617c79b96"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s] %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)

toggl_datetime_format = "%Y-%m-%dT%H:%M:%S+00:00"

start_date = datetime.strftime(
    datetime.now().replace(month=MONTH, day=1, hour=0, minute=0, second=0, year=2025),
    toggl_datetime_format,
)
end_date = datetime.strftime(
    datetime.now().replace(day=1, hour=0, minute=0, second=0), toggl_datetime_format
)

logger.info("Authenticating on Toggl...")
toggl: Toggl = Toggl()
toggl.setAPIKey(TOGGL_API_TOKEN)
logger.info("Successfully authenticated on Toggl")

logger.info(f"Getting Toggl`s entries month {MONTH}")

wb = load_workbook("template.xlsx")

ws = wb.active
projects = {}
workspace_id = None
try:
    query_params = f"start_date={urllib.parse.quote(start_date)}&end_date={urllib.parse.quote(end_date)}&meta=true"
    print(f"https://api.track.toggl.com/api/v9/me/time_entries?{query_params}")
    response = toggl.request(
        f"https://api.track.toggl.com/api/v9/me/time_entries?{query_params}"
    )

    workspace_response = toggl.getWorkspaces()
    logger.info(workspace_response)
    logger.info(workspace_response.text())
    workspace_id = workspace_response[0]["id"]
except Exception as e:
    logger.error(e)
    SystemExit()

response.sort(key=lambda item: item["start"].lower())

logger.info(f"{len(response)} log entries located on defined time range")
logged_entries = 0
for entry in response:
    current = {}
    # if "tags" not in entry or "logged" not in entry["tags"]:
    try:
        logger.warning(entry)
        logger.warning(projects)
        if entry["pid"] not in projects:
            projects[entry["pid"]] = {
                "name": entry["project_name"],
                "url": [url for url in entry["tags"] if "https://" in url][0],
            }
        current = projects[entry["pid"]]

        logger.info(
            f'Adding worklog from project {current["name"]}'
            + f' of {str(timedelta(seconds=entry["duration"]))} on {entry["start"]}'
        )
        logger.warning(current["name"])
        ws.cell(row=logged_entries + 2, column=1).value = current["name"]
        ws.cell(row=logged_entries + 2, column=2).value = (
            current["url"]
            if not entry["tags"]
            else [url for url in entry["tags"] if "https://" in url][0]
        )
        ws.cell(row=logged_entries + 2, column=3).value = datetime.fromisoformat(
            entry["start"]
        ).strftime("%d/%m")
        ws.cell(row=logged_entries + 2, column=5).value = str(
            timedelta(seconds=entry["duration"])
        )

        logger.info("Sucessfull\n")
        logger.info('Adding "logged" tag on Toggl entry')
        if "tags" in entry:
            entry["tags"].append("logged")
        else:
            entry["tags"] = ["logged"]
        data = {"time_entry": entry}
        # new_r = toggl.postRequest(
        #     f'https://api.track.toggl.com/api/v8/time_entries/{entry["id"]}',
        #     parameters=data, method='PUT'
        # )
        logger.info("Sucessfull\n")
        logged_entries += 1
    except Exception as e:
        logger.error(
            f'Error on {entry["id"]} of {float(entry["duration"])/3600:.2f}h on {entry["start"]}'
        )
        logger.error(e)
        logger.error(traceback.format_exc())
        sys.exit(1)

wb.save("output.xlsx")
logger.info(f"Logged hours on JIRA of {logged_entries} entries")
logger.info("Ending Auto-logger execution")
