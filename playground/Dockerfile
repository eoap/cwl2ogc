# Use an official Python base image
FROM python:3.11-slim

# Set environment variables to reduce image size
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install streamlit cwl2ogc>=0.4.0 streamlit_code_editor
# Copy app code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "playground.py", "--server.port=8501", "--server.address=0.0.0.0"]
