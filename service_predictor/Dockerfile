
# Dockerfile

FROM python:3.8

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH to include the current working directory
ENV PYTHONPATH /app

# Copy the db_package directory
# Set the PYTHONPATH to include the current working directory and db_package
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/db_package"

# Copy the rest of the application code
COPY . .

# Command to run your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
