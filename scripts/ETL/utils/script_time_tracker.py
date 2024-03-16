import json, datetime, pytz

class ScriptTimeTracker:
  def track_time(self, script_name):
    pst = pytz.timezone('America/Los_Angeles')
    current_time = datetime.datetime.now(pst).isoformat()
    with open('script_history.json', 'r+') as file:
      data = json.load(file)
      data[script_name] = current_time
      file.seek(0)
      json.dump(data, file, indent=4)
      file.truncate()
