FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
EXPOSE 8001
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV REPORT_SERVICE_URL=http://0.0.0.0:8001/generate_report/
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# sudo docker build -t codeanalytics-backend .
# docker run -d -p 8000:8000 --network my_network --name codeanalytics-backend -e REPORT_SERVICE_URL="http://report-service:8001/generate_report/" codeanalytics-backend