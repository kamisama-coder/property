# Use Python base image
FROM python:3.12.4

# Set working directory inside container
WORKDIR /app

# Copy backend files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/openai/CLIP.git
# Expose the backend port (change if needed)

# Run the app (change app.py and port if needed)
CMD ["python", "server.py"]
