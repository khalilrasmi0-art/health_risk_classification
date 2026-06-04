# 🚀 DEPLOYMENT GUIDE

Your Health Risk Classification app can be deployed on multiple platforms. Here are the recommended options:

---

## 🎯 **RECOMMENDED: Deploy on Streamlit Cloud (FREE)**

Streamlit Cloud is the **easiest and best option** for Streamlit apps.

### Steps:

1. **Sign up at:** https://streamlit.io/cloud
2. **Connect your GitHub repository**
3. **Select your repository:** `health_risk_classification`
4. **Configure deployment:**
   - Main file path: `app.py`
   - Python version: 3.10
5. **Deploy!** ✅

Your app will be live in minutes at: `https://<your-username>-health-risk-classification.streamlit.app`

---

## 🐳 **Alternative: Deploy on Heroku (Paid)**

### Steps:

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

5. Open your app:
   ```bash
   heroku open
   ```

---

## ☁️ **Alternative: Deploy on Railway (Easy)**

### Steps:

1. Go to: https://railway.app
2. Click "Deploy on Railway"
3. Select GitHub repository
4. Configure environment
5. Deploy!

---

## 🐳 **Alternative: Deploy with Docker**

### Create Docker image:

1. Build:
   ```bash
   docker build -t health-risk-app .
   ```

2. Run locally:
   ```bash
   docker run -p 8501:8501 health-risk-app
   ```

3. Push to Docker Hub or deploy to cloud

---

## ✅ **LOCAL DEPLOYMENT (Development)**

### Run locally:

```bash
cd health_risk_classification
./venv/Scripts/Activate.ps1
streamlit run app.py
```

Then open: `http://localhost:8501`

---

## 📋 **TROUBLESHOOTING**

### Issue: "Page not found" on Netlify
**Solution:** Netlify doesn't support Python/Streamlit apps. Use Streamlit Cloud instead.

### Issue: Dependencies not installing
**Solution:** Ensure `requirements.txt` is in the root directory with compatible versions.

### Issue: Model files not found
**Solution:** Make sure `.pkl` files are in the repository and not in `.gitignore`.

---

## 🔍 **WHAT GETS DEPLOYED**

✅ app.py
✅ best_model.pkl
✅ preprocessing_info.pkl
✅ feature_names.pkl
✅ requirements.txt
✅ All supporting files

---

## 📊 **DEPLOYMENT READINESS CHECKLIST**

- ✅ `requirements.txt` - Updated with compatible versions
- ✅ Model files (`.pkl`) - Included in repo
- ✅ `app.py` - Streamlit interface configured
- ✅ `.streamlit/config.toml` - Configuration file
- ✅ GitHub Actions CI/CD - Workflow configured
- ✅ `Procfile` - Heroku deployment config
- ✅ `.gitignore` - Properly configured

---

## 🎯 QUICK DEPLOYMENT COMMANDS

### Streamlit Cloud
```bash
# Just push to GitHub, Streamlit Cloud handles the rest!
git push origin main
```

### Local Testing
```bash
streamlit run app.py
```

### Heroku Deployment
```bash
heroku login
heroku create app-name
git push heroku main
```

---

**Status:** ✅ **READY FOR DEPLOYMENT**

Choose your platform and deploy! 🚀
