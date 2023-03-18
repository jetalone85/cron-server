import subprocess

# Replace the path and filename with the path to your Python script
cmd = ["python", "./notification.py"]

# Use subprocess to start the script as a background task
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Print the process ID (PID) of the background task
print("Background task started with PID:", process.pid)
