FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
# EXPOSE 8082

CMD ["streamlit", "run", "index.py", "--server.port=8080", "--server.address=0.0.0.0"]
# CMD ["streamlit", "run", "index.py", "--server.port=8082", "--server.address=0.0.0.0"]

# sudo docker build -t codeanalytics-frontend .
# docker run -d -p 8080:8080 --name codeanalytics-frontend codeanalytics-frontend (cloud)
# docker run -d -p 8082:8082 --network my_network --name codeanalytics-frontend codeanalytics-frontend (locale)
