import json, datetime, pytz

class ScriptTimeTracker:
  pst = pytz.timezone('America/Los_Angeles')
  current_time = datetime.datetime.now(pst).isoformat()

  def track_time(self, script_name):
    with open('script_history.json', 'r+') as file:
      data = json.load(file)
      if f"{script_name}_First" not in data:
          data[f"{script_name}_First"] = self.current_time
      data[f"{script_name}_Last"] = self.current_time
      file.seek(0)
      json.dump(data, file, indent=4)
      file.truncate()
