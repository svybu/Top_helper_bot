FROM python:3.9-slim-buster
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
WORKDIR ./app
COPY top_helper_bot .
VOLUME ./notes
CMD ["python", "menu.py"]
