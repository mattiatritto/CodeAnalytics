FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
# sudo docker build -t report-service .
# docker run -d -p 8001:8001 --network my_network  --name report-service report-service