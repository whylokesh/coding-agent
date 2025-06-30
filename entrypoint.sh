#!/bin/bash

# Start X virtual framebuffer
Xvfb :1 -screen 0 1024x768x16 &
export DISPLAY=:1

# Wait a bit for Xvfb to properly initialize
sleep 2

# Start window manager
fluxbox &

# Start xterm (GUI terminal)
xterm &

# Start file manager (optional)
pcmanfm &

# Wait a bit more to ensure DISPLAY is ready
sleep 2

# Set up x11vnc to attach to display :1 and use password file
x11vnc -display :1 -rfbauth /root/.vnc/passwd -forever -shared -bg

# Run websockify to proxy :6080 → :5901 (VNC port for :1)
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

# Finally, start the FastAPI app
uvicorn api.orchestrator:app --host 0.0.0.0 --port 8000
