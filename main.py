import subprocess
import os
import select
import json
import time
from pathlib import Path

from sensor import IMU_Sensor

imu_sensor = IMU_Sensor()

os.environ['DISPLAY'] = ":0"
# region Setup pipes and renderer
# Start the renderer program as a child process
renderer_path = Path(os.path.normpath("../OpenWiXR-Renderer/")).resolve()
renderer_path_bin = renderer_path.joinpath("_bin/Debug/")
renderer_process = subprocess.Popen(os.path.join(renderer_path_bin, "OpenWiXR-Renderer"), cwd=renderer_path)

to_core_pipe_path = "/tmp/to_core"
if os.path.exists(to_core_pipe_path):
    os.remove(to_core_pipe_path)
os.mkfifo(to_core_pipe_path)
to_core_pipe_fd = os.open(to_core_pipe_path, os.O_RDWR | os.O_NONBLOCK)

to_renderer_pipe_path = "/tmp/to_renderer"
if os.path.exists(to_renderer_pipe_path):
    os.remove(to_renderer_pipe_path)
os.mkfifo(to_renderer_pipe_path)
to_renderer_pipe_fd = os.open(to_renderer_pipe_path, os.O_RDWR | os.O_NONBLOCK)
# endregion

# Run the raylib loop
while True:
    # Check if the pipe is ready for reading or writing
    read_ready, write_ready, _ = select.select([to_core_pipe_fd], [to_renderer_pipe_fd], [], 0)

    if read_ready:
        # Read the message from the renderer
        message = os.read(to_core_pipe_fd, 1024)
        messages = list(filter(lambda s: len(s) > 0, message.decode().split("\0")))
        for m in messages:
            if m:
                # Process the received message
                try:
                    data = json.loads(m)
                except Exception as e:
                    print(e)
                    continue

                # print("==CORE== Received message from Renderer:")
                # print("\tType:", data["type"])
                # print("\tData:", data["data"])

    if write_ready:
        # Send a message to the renderer
        # message = {
        #     "type": "Greeting",
        #     "data": "Hello, Renderer!"
        # }
        data = imu_sensor.get_data()
        message = {
            "type": "Sensor",
            "data": data
        }
        # print(message)
        os.write(to_renderer_pipe_fd, json.dumps(message).encode())

    time.sleep(float(1/60))
    # Add any necessary synchronization mechanisms if needed

# Close the pipe
os.close(to_renderer_pipe_fd)

# Wait for the renderer process to finish
renderer_process.wait()
