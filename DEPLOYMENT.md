# 🚀 Deployment Guide - Email Spam Detector

Complete guide for deploying the Email Spam Detector to production environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platforms](#cloud-platforms)
4. [Performance Optimization](#performance-optimization)
5. [Monitoring & Logging](#monitoring--logging)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Setup

```bash
# Clone repository
git clone <repository-url>
cd Email\ Spam\ Detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK resources
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Run application
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Development Configuration

Create `.streamlit/secrets.toml` for local development:
```toml
[development]
debug = true
log_level = "debug"
```

---

## Docker Deployment

### Build Docker Image

```bash
# Build image
docker build -t spam-detector:latest .

# Tag for registry
docker tag spam-detector:latest your-registry/spam-detector:latest
```

### Run Docker Container

```bash
# Run locally
docker run -p 8501:8501 spam-detector:latest

# Run with volume mounts
docker run -p 8501:8501 \
  -v $(pwd)/Data:/app/Data:ro \
  -v $(pwd)/Models:/app/Models:ro \
  spam-detector:latest

# Run with environment variables
docker run -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  spam-detector:latest
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f spam-detector

# Stop services
docker-compose down
```

### Docker Image Optimization

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## Cloud Platforms

### Streamlit Cloud (Recommended for Quick Deployment)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Choose branch and file (`app.py`)
   - Click "Deploy"

3. **Configure Secrets** (in Streamlit Cloud dashboard)
   ```toml
   [database]
   url = "your-database-url"
   
   [api]
   key = "your-api-key"
   ```

### AWS Deployment

#### Option 1: EC2 + Docker

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker

# Clone and run
git clone <repository-url>
cd Email\ Spam\ Detector
docker-compose up -d
```

#### Option 2: AWS App Runner

```bash
# Create ECR repository
aws ecr create-repository --repository-name spam-detector

# Push image
docker tag spam-detector:latest <account-id>.dkr.ecr.<region>.amazonaws.com/spam-detector:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/spam-detector:latest

# Create App Runner service via AWS Console
# Select ECR image and configure
```

#### Option 3: AWS Lambda + API Gateway

```python
# lambda_handler.py
from mangum import Mangum
from app import main

handler = Mangum(main)
```

### Google Cloud Deployment

#### Cloud Run

```bash
# Authenticate
gcloud auth login

# Build and push
gcloud builds submit --tag gcr.io/your-project/spam-detector

# Deploy
gcloud run deploy spam-detector \
  --image gcr.io/your-project/spam-detector \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2
```

#### App Engine

```yaml
# app.yaml
runtime: python311
env: standard

entrypoint: streamlit run app.py --server.port 8080

env_variables:
  STREAMLIT_SERVER_PORT: "8080"
  STREAMLIT_SERVER_ADDRESS: "0.0.0.0"
```

```bash
gcloud app deploy
```

### Azure Deployment

#### Container Instances

```bash
# Create resource group
az group create --name spam-detector-rg --location eastus

# Create container
az container create \
  --resource-group spam-detector-rg \
  --name spam-detector \
  --image your-registry.azurecr.io/spam-detector:latest \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_PORT=8501
```

#### App Service

```bash
# Create App Service plan
az appservice plan create \
  --name spam-detector-plan \
  --resource-group spam-detector-rg \
  --sku B2 --is-linux

# Create web app
az webapp create \
  --resource-group spam-detector-rg \
  --plan spam-detector-plan \
  --name spam-detector-app \
  --deployment-container-image-name your-registry.azurecr.io/spam-detector:latest
```

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create spam-detector

# Add buildpack
heroku buildpacks:add heroku/python

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

## Performance Optimization

### Caching Strategy

```python
# Use Streamlit caching effectively
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_model():
    return load_model()

@st.cache_resource  # Cache for session lifetime
def get_database_connection():
    return connect_to_db()
```

### Resource Limits

```yaml
# docker-compose.yml
services:
  spam-detector:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Load Balancing

```nginx
# nginx.conf
upstream spam_detector {
    server app1:8501;
    server app2:8501;
    server app3:8501;
}

server {
    listen 80;
    location / {
        proxy_pass http://spam_detector;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

### Health Checks

```python
# health_check.py
import requests

def check_health():
    try:
        response = requests.get('http://localhost:8501/_stcore/health')
        return response.status_code == 200
    except:
        return False
```

### Monitoring with Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'spam-detector'
    static_configs:
      - targets: ['localhost:8501']
```

### Logging with ELK Stack

```yaml
# docker-compose.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

#### Model Files Not Found
```bash
# Verify file structure
ls -la Models/
# Should show: model.pkl, vectorizer.pkl

# Download if missing
# (Provide download link or script)
```

#### NLTK Resources Missing
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

#### Memory Issues
```bash
# Increase Docker memory
docker run -m 4g spam-detector:latest

# Or in docker-compose.yml
services:
  spam-detector:
    deploy:
      resources:
        limits:
          memory: 4G
```

#### Slow Performance
1. Check CPU/Memory usage: `docker stats`
2. Enable caching: Use `@st.cache_data` and `@st.cache_resource`
3. Optimize model: Use smaller vectorizer or quantized model
4. Add load balancer: Distribute traffic across multiple instances

### Debug Mode

```bash
# Run with debug logging
streamlit run app.py --logger.level=debug

# Or set environment variable
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run app.py
```

### Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

---

## Security Best Practices

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Environment Variables**: Store secrets in `.env` or cloud provider secrets
3. **Input Validation**: Validate all user inputs
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **CORS**: Configure CORS properly for cross-origin requests
6. **Dependencies**: Keep dependencies updated
7. **Secrets Management**: Use AWS Secrets Manager, Azure Key Vault, etc.

---

## Scaling Strategies

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use container orchestration (Kubernetes)
- Implement session persistence

### Vertical Scaling
- Increase CPU/Memory allocation
- Optimize code and algorithms
- Use faster hardware

### Database Scaling
- Use read replicas
- Implement caching layer (Redis)
- Partition data

---

## Maintenance

### Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update Docker image
docker pull python:3.11-slim
docker build -t spam-detector:latest .
```

### Backup Strategy
```bash
# Backup models and data
tar -czf backup-$(date +%Y%m%d).tar.gz Models/ Data/

# Upload to cloud storage
aws s3 cp backup-*.tar.gz s3://your-bucket/backups/
```

---

## Support & Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-cloud/deploy-your-app)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Deployment Guide](https://aws.amazon.com/getting-started/)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Azure Documentation](https://docs.microsoft.com/azure/)

---

**Last Updated**: 2024
