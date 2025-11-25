# JIRA + Toggl Auto Logger
This repository has a simple python script that creates worklogs on JIRA based on entries/timelogs on Toggl.

> (i) The name/description of your Toggl entry must be equal to the JIRA's Issue ID (eg. **PROJ-111**)

# Configuration
## Python Requirements
You need python 3.0+ for this project to be run on your machine.
All requirements are listed on the *requirements.txt* file. You can install all the requirements of this project using pip as decribed below :

Linux:
```
> $ python3 -m venv venv # Optional (but recommended) creation of virtual environment for the project
> $ source venv/bin/activate # Activation of the created virtual environment
> $ pip install -r requirements.txt # Recursively install all requirements listed on file
```

Windows:
```
> $ python3 -m venv venv # Optional but recommended creation of virtual environment for the project
> $ .\venv\Scripts\activate.bat # Activation of the created virtual environment
> $ pip install -r requirements.txt # Recursively install all requirements listed on file
```

> For the deactivation of the virtual environment, for both Windows and Linux, simply execute ```$ deactivate``` on the terminal.

## Tokens
You need to provide some tokens and informations that allows the code to sucessfully authenticate and manage timelogs on your JIRA and Toggl accounts. These informations need to be set to the related variable, which are:
### TOGGL_API_TOKEN

Toggl's API token, to allow the script to use the Toggl's API to get your log entries. This can be found in your [Profile Page](https://track.toggl.com/profile):

![Toggl profile path](https://i.imgur.com/nVktHF7.png)
![Toggl API key](https://i.imgur.com/4CV2RF8.png)

### JIRA_SERVER

The complete url of your JIRA server, eg. *https://yourcompanyname.atlassian.net*

### JIRA_MAIL

Your JIRA user e-mail

### JIRA_API_TOKEN

JIRA's API token, to allow the script to use the JIRA's API to log your time entries. This can be found in your [Account Settings > Security > Create and manage API tokens](https://id.atlassian.com/manage-profile/security/api-tokens):

![JIRA profile path](https://i.imgur.com/jqalxbi.png)
![JIRA profile path 2](https://i.imgur.com/WAm9ZwJ.png)
![JIRA token creation](https://i.imgur.com/TuX0dR6.png)

### TIME_DELTA_DAYS
The Toggl's entries time delta related to the day of script execution. It represents the quantity of days before the moment of execution that will be considered for all the worklog entries.

# Executing the Script
After installing all the requirements and setting all the required variables to their correct values, you can simply run the *main.py* script with your python command:

```
$ python main.py
```

There are (rudimentary) logs that will be displayed on the terminal executing the script, which can be used for debuging.

# Limitations
- The Toggl's entry name/description must be the same as the JIRA's Issue ID
- The script controls which entries were logged using a tag named '*logged*'
- No worklog description can be logged on JIRA
- No error management