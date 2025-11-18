# Use a lightweight Python base image
# Keep your existing CMD ["python", "organizer.py"]
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies directly (bypasses any requirements.txt issues)
RUN pip install --no-cache-dir PyYAML

# Copy your files into the container
COPY organizer.py config.yaml ./

# Run the script when the container starts
CMD ["python", "organizer.py"]