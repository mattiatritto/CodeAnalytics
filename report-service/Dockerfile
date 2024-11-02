FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
# docker network create my_network
# sudo docker build -t report-service .
# docker run -d -p 8080:8080 --network my_network  --name report-service report-service