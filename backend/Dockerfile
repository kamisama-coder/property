# Use Python base image
FROM python:3.12.4

# Set working directory inside container
WORKDIR /app

# 1. Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/openai/CLIP.git

# 3. Copy the rest of the application code
COPY . .

# Run the app
CMD ["python", "server.py"]