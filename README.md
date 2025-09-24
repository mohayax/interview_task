#  Interview Task - Blog API

A simple Blog API built with **Django + PostgreSQL + Docker**.  
This project includes authentication, blog posts, comments, and likes functionality.  

## Features
- User authentication  
- Blog posts with title, body, cover photo (uploaded to google cloud bucket), author, and likes  
- Comments on blog posts  
- PostgreSQL database (Dockerized for local dev)  
- Ready for deployment on **Render** with GitHub Actions CI/CD  

---

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mohayax/interview_task.git
cd interview_task

## build and start
docker-compose up --build -d

## run migrations
docker-compose exec web python manage.py migrate


## .env 
GS_BUCKET_NAME=your-bucket-name
GCS_JSON_CONTENT='{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOURKEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account"
}'

SECRET_KEY=your-secret-key

