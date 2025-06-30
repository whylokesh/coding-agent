# Base image with Python
FROM python:3.11-slim

# System dependencies + Node.js + GUI tools
RUN apt-get update && apt-get install -y \
    curl sudo git vim build-essential \
    xvfb x11vnc fluxbox xdotool \
    net-tools novnc websockify \
    tightvncserver gnupg \
    xterm pcmanfm \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Confirm Node and npm versions (for debugging)
RUN node -v && npm -v

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Setup VNC password
RUN mkdir -p /root/.vnc && \
    echo "password" | vncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd

# Copy and prepare entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose FastAPI + noVNC
EXPOSE 8000 6080 5901

# Start app + VNC GUI
CMD ["/entrypoint.sh"]
