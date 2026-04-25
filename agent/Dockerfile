FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/nexaryn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./agent

CMD ["python", "-m", "agent.main"]
