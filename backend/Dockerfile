FROM python:3.10-slim
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ffmpeg libavcodec-extra -y
WORKDIR /app/
COPY backend/ .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]