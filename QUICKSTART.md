# 🚀 Quick Start Guide

Get the Email Spam Detector running in 5 minutes!

## Option 1: Local Development (Fastest)

### Step 1: Clone & Setup
```bash
# Clone repository
git clone https://github.com/your-username/Email-Spam-Detector.git
cd Email\ Spam\ Detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download NLTK Resources
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Step 3: Run the App
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` 🎉

---

## Option 2: Docker (Recommended for Production)

### Step 1: Build Image
```bash
docker build -t spam-detector:latest .
```

### Step 2: Run Container
```bash
docker run -p 8501:8501 spam-detector:latest
```

Access at `http://localhost:8501` 🎉

### Or Use Docker Compose
```bash
docker-compose up -d
```

---

## Option 3: Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your repository
5. Deploy! 🎉

---

## First Steps

### 1. Analyze a Message
- Go to **Home** page
- Paste an email or SMS
- Click **"🔍 Analyze Message Now"**
- View results with confidence score

### 2. Upload Email File
- Click file upload area
- Select `.eml` or `.txt` file
- Click **"🔍 Analyze Message Now"**
- See email metadata and analysis

### 3. Batch Analysis
- Upload multiple files
- Click **"🔍 Analyze Message Now"**
- View summary and individual results

### 4. Explore Features
- **About**: Learn how it works
- **Help**: Get usage tips
- **Contact**: Reach out to team

---

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### NLTK Resources Missing
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Model Files Not Found
Ensure `Models/model.pkl` and `Models/vectorizer.pkl` exist

### Memory Issues
```bash
# Increase Docker memory
docker run -m 4g -p 8501:8501 spam-detector:latest
```

---

## Next Steps

1. **Read Documentation**
   - [README.md](README.md) - Full documentation
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide

2. **Explore Code**
   - `src/pages/home.py` - Main detector
   - `src/model.py` - ML model
   - `src/nlp.py` - NLP processing

3. **Deploy to Cloud**
   - [Streamlit Cloud](https://share.streamlit.io)
   - [AWS](DEPLOYMENT.md#aws-deployment)
   - [Google Cloud](DEPLOYMENT.md#google-cloud-deployment)
   - [Azure](DEPLOYMENT.md#azure-deployment)

4. **Contribute**
   - Check [CONTRIBUTING.md](CONTRIBUTING.md)
   - Fork repository
   - Create feature branch
   - Submit pull request

---

## Key Features

✨ **AI-Powered Detection**
- 97%+ accuracy
- Real-time analysis
- Confidence scores

🧠 **Smart Explanations**
- Word impact analysis
- Top spam/ham indicators
- Feature breakdown

📧 **Email Support**
- Parse .eml files
- Extract metadata
- Check authentication

📊 **Batch Processing**
- Analyze multiple files
- Summary statistics
- Export results

🎨 **Beautiful UI**
- Dark theme
- Responsive design
- Smooth animations

🔐 **Privacy First**
- No data storage
- Local processing
- No external APIs

---

## System Requirements

- **Python**: 3.8+
- **RAM**: 2GB minimum (4GB recommended)
- **Disk**: 500MB for dependencies
- **OS**: Windows, macOS, Linux

---

## Performance

- **Inference Time**: <100ms per message
- **Accuracy**: 97%+
- **Throughput**: 100+ messages/minute
- **Memory**: ~500MB

---

## Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/your-username/Email-Spam-Detector/issues)
- 💬 [Discussions](https://github.com/your-username/Email-Spam-Detector/discussions)
- 📧 [Email Support](mailto:support@spamdetector.ai)

---

## License

MIT License - See [LICENSE](LICENSE) file

---

**Happy spam detecting! 🛡️**
