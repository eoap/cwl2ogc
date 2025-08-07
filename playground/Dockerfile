# Use an official Python base image
FROM python:3.11-slim

# Set environment variables to reduce image size
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set up a default user and home directory
ENV HOME=/home/neo

# Create a user with UID 1001, group root, and a home directory
RUN groupadd -g 2000 neo && \
    useradd -u 2000 -r -g 2000 -m -d ${HOME} -s /sbin/nologin \
      -c "Default Neo User" neo && \
    mkdir -p /app && \
    mkdir -p ${HOME}/.cache && \
    chown -R 2000:2000 /app ${HOME} && \
    chmod g+rwx ${HOME} /app

# Switch to the non-root user
USER neo


# Copy the application files into the /code directory
COPY --chown=2000:2000 . /app

# Set working directory
WORKDIR /app


# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install streamlit streamlit_code_editor cwltool
# Copy app code
COPY --chown=2000:2000 . .

# Expose Streamlit default port
EXPOSE 8501

ENV PATH="/home/neo/.local/bin:${PATH}"

# Run Streamlit app
CMD ["streamlit", "run", "playground/playground.py", "--server.port=8501", "--server.address=0.0.0.0"]
