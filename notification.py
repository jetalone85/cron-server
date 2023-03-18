import os
from time import sleep


notification_title = "Report Generation"
notification_subtitle = "All reports have been generated successfully"
notification_message = "Task completed"
notification_sound = "Submarine"

command = f'osascript -e \'display notification "{notification_message}" with title "{notification_title}" subtitle "{notification_subtitle}" sound name "{notification_sound}"\''

os.system(command)
