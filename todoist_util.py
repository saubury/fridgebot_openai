from todoist_api_python.api import TodoistAPI
from config_secrets import TODOIST

def add_task(task_name):
    api_key = TODOIST['api_token']
    project_id = TODOIST['project_id']

    api = TodoistAPI(api_key)
    task = api.add_task(content=task_name, project_id=project_id)



