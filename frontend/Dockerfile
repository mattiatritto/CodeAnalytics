FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]
# sudo docker build -t codeanalytics-frontend .
# docker run -d -p 8501:8501 --network my_network --name codeanalytics-frontend codeanalytics-frontend