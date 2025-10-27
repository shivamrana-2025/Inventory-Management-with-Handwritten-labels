# 🛒 Handwritten Inventory Management (Local + Colab)

### 📦 Features
- Upload handwritten labels (e.g. 'Apple Qty: 6 Price: 100')
- Automatically extract Item, Quantity, and Price using TrOCR
- Manual correction support
- Real-time inventory table

### ▶️ Local Usage
```bash
pip install -r requirements.txt
streamlit run app_frontend.py
```

### ☁️ Colab Usage
```python
!pip install -r requirements.txt
from pyngrok import ngrok
public_url = ngrok.connect(8501)
print(public_url)
!streamlit run app_frontend.py --server.port 8501 &
```
