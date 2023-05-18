FROM python:3.10-slim
RUN apt update
RUN apt upgrade
RUN apt install ffmpeg libavcodec-extra -y
WORKDIR /app/
COPY backend/ .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]