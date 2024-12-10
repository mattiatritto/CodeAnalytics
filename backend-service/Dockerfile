FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV REPORT_SERVICE_URL=https://report-service-image-771804227712.us-central1.run.app/generate_report/ 
# docker run -d -p 8080:8080 --network my_network --name codeanalytics-backend -e REPORT_SERVICE_URL="https://report-service-image-771804227712.us-central1.run.app/generate_report/" codeanalytics-backend (cloud)
# ENV REPORT_SERVICE_URL=http://report-service:8081/generate_report/
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

# sudo docker build -t codeanalytics-backend .
# docker run -d -p 8080:8080 --network my_network --name codeanalytics-backend -e REPORT_SERVICE_URL="http://report-service:8081/generate_report/" codeanalytics-backend