FROM python:3.11.2

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy the model file into a specific directory within the container
COPY prophet_model.pkl /usr/src/app/models/prophet_model.pkl

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]