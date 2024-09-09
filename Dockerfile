# Parent image
FROM python:3.9-slim

WORKDIR /usr/src/app

# Copies all working directory contents on local machine to the container
COPY . .


RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "./main.py"]
