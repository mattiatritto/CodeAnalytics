# CodeAnalytics

CodeAnalytics is an AI-powered tool designed to estimate the duration and costs of software projects based on various input parameters. Leveraging machine learning models, the software provides accurate predictions using Adjusted Function Points (AFP) methodology. This approach helps project managers and developers gain insights into resource planning and budgeting, allowing for more effective and efficient project execution.

## Server execution on local machine

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:
   Clone the project from the GitHub repository using the following command:

   ```
   git clone https://github.com/mattiatritto/CodeAnalytics.git
   ```
   
   
2. **Navigate to the project directory**: Change into the project directory:

   ```
   cd CodeAnalytics
   ```

3. **Build the Docker image**: Build the Docker image for the project using the command below:

   ```
   sudo docker build -t CodeAnalytics .
   ```

4. **Run the Docker container**: After building the Docker image, you can run the project by executing the following command:

   ```
   docker run -d -p 8080:8080 --name CodeAnalytics CodeAnalytics
   ```

## Server deployment on Google Cloud Platform

To deploy the server on Google Cloud Platform, follow these steps:

1. **Install Google Cloud CLI**:
   Install the `gcloud` CLI by following the instructions at the [official documentation](https://cloud.google.com/sdk/docs/install).

2. **Create a new Google Cloud project**:
   Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project, named CodeAnalytics

3. **Enable required services**:
   Enable the following APIs and services in your project:
   
   - `Artifact Registry API`
   - `Cloud Build`
   - `Cloud Deploy`

   You can do this by searching for these services in the Google Cloud Console and enabling them.

4. **Authenticate with Google Cloud**:
   Log in to your Google Cloud account using the `gcloud` CLI:

   ```
   gcloud auth login
   ```
   
4. **Set the project in your gcloud CLI**:
   Set your project as the active one by running:

   ```
   gcloud config set project CodeAnalytics
   ```

6. **Create an Artifact Registry**:
   Create a new Docker repository in the Artifact Registry to store your Docker images:

   ```
   gcloud artifacts repositories create CodeAnalytics \
    --repository-format=docker \
    --location=us-central1 \
    --description="CodeAnalytics backend"
   ```

6. **Build and submit the Docker image**: 
   Use Cloud Build to build and submit your Docker image to the Artifact Registry:

   ```
    gcloud builds submit --region=us-central1 \
    --tag us-central1-docker.pkg.dev/CodeAnalytics/CodeAnalytics/CodeAnalytics-image:tag1
   ```

7. **Deploy the Docker image to Cloud Run**: 
   Deploy the Docker image to Cloud Run, which will host your service:

   ```
    gcloud run deploy --image=us-central1-docker.pkg.dev/CodeAnalytics/CodeAnalytics/CodeAnalytics-image:tag1
   ```

8. **Verify the deployment**: 
   Once deployed, you can check if the service is running by accessing the following URL:

   ```
    https://CodeAnalytics-image-5699838011.us-central1.run.app/docs
   ```


## Software Architecture Overview

1. **Frontend (Streamlit)**
   - Users interact with the application through a web interface built using Streamlit.
   - The frontend sends requests to the backend to process data or obtain predictions from the Machine Learning model.

2. **Backend (FastAPI)**
   - The backend is built using FastAPI, which handles requests from the frontend.
   - It interacts with the Machine Learning model to make predictions.
   - The backend provides various endpoints for functionalities such as sending data for predictions and receiving past data in order to make analytics.

3. **Containerization (Docker)**
   - The backend is containerized using Docker.
   - This ensures that the application runs consistently across different environments.

4. **Cloud Deployment**
   - The application is deployed in the cloud using services like Google Cloud Platform.



   
   


   