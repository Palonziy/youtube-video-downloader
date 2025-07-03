# YouTube Video Downloader - Tezkor Ishga Tushirish

## Loyiha Tuzilishi
```
youtube-downloader-complete/
├── backend/           # Flask backend server
├── frontend/          # React frontend interface  
└── README.md         # To'liq loyiha hujjati
```

## Tezkor Ishga Tushirish

### 1. Backend Serverni Ishga Tushirish
```bash
cd backend
source venv/bin/activate
python src/main.py
```
✅ Server http://localhost:5001 da ishga tushadi

### 2. Frontend Interfeysi Ishga Tushirish
```bash
cd frontend
npm install  # (agar kerak bo'lsa)
npm run dev
```
✅ Frontend http://localhost:5174 da ishga tushadi

### 3. Saytdan Foydalanish
1. Brauzerda http://localhost:5174 ga o'ting
2. YouTube video havolasini kiriting
3. "Tahlil qilish" tugmasini bosing
4. Kerakli formatni tanlab "Yuklab olish" tugmasini bosing

## Muhim Eslatmalar

⚠️ **Huquqiy jihatlar**: Faqat shaxsiy foydalanish uchun. Mualliflik huquqlarini hurmat qiling.

🔧 **Texnik talablar**: Python 3.11+, Node.js 18+, 1GB RAM

📊 **Ma'lumotlar bazasi**: SQLite (backend/src/database/app.db) da foydalanuvchi faoliyati saqlanadi

## Qo'shimcha Ma'lumotlar

To'liq texnik hujjat va API ma'lumotlari uchun README.md faylini o'qing.

