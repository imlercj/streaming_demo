# Use a minimal Python base image
FROM python:3.10-alpine

# Install system dependencies and build tools
RUN apk add --no-cache python3 postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev linux-headers

# Install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Install JupyterLab
RUN pip install --no-cache-dir jupyterlab

# Clean up build dependencies
RUN apk --purge del .build-deps

# Set up a workspace directory (will be mounted)
WORKDIR /workspace

# Expose JupyterLab's default port
EXPOSE 8888

# Start JupyterLab on container startup
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
