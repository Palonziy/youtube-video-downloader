# YouTube Video Downloader - Loyiha Hujjati

## Loyiha Tavsifi

YouTube Video Downloader - bu zamonaviy, interaktiv va responsive veb-sayt bo'lib, foydalanuvchilarga YouTube videolarini turli formatlar va sifatlarda yuklab olish imkoniyatini beradi. Sayt to'liq funksional bo'lib, foydalanuvchi faoliyatini kuzatish va ma'lumotlar bazasiga yozish imkoniyatlari bilan jihozlangan.

## Texnik Xususiyatlar

### Backend (Flask)
- **Framework**: Flask 3.1.1
- **Video yuklab olish**: yt-dlp kutubxonasi
- **Ma'lumotlar bazasi**: SQLite
- **CORS qo'llab-quvvatlash**: Flask-CORS
- **API endpointlari**:
  - `GET /api/health` - Server holatini tekshirish
  - `POST /api/get_video_info` - Video ma'lumotlarini olish
  - `POST /api/download_video` - Videoni yuklab olish

### Frontend (React)
- **Framework**: React 18 + Vite
- **UI Kutubxonalari**: Tailwind CSS, shadcn/ui
- **Animatsiyalar**: Framer Motion
- **Ikonlar**: Lucide React
- **Responsive dizayn**: Mobil va desktop qurilmalar uchun optimallashtirilgan

### Ma'lumotlar Bazasi
- **Tizim**: SQLite
- **Jadvallar**:
  - `video_info_requests` - Video ma'lumotlari so'rovlari
  - `download_logs` - Yuklab olish loglari
  - `users` - Foydalanuvchilar (kelajakda)

## Funksional Imkoniyatlar

### Asosiy Funksiyalar
1. **Video Ma'lumotlarini Olish**
   - YouTube URL ni tahlil qilish
   - Video sarlavhasi, muallifi, davomiyligi
   - Thumbnail rasmi
   - Mavjud formatlar va sifatlar ro'yxati

2. **Video Yuklab Olish**
   - Turli sifat variantlari (360p, 720p, 1080p va boshqalar)
   - Turli formatlar (MP4, WEBM)
   - Fayl hajmi ma'lumotlari
   - To'g'ridan-to'g'ri brauzer orqali yuklab olish

3. **Foydalanuvchi Kuzatuvi**
   - IP manzil va User-Agent saqlash
   - So'rovlar vaqti va holati
   - Yuklab olingan videolar statistikasi
   - Xatoliklar logi

### Xavfsizlik Xususiyatlari
- URL validatsiyasi
- Xatoliklarni to'g'ri boshqarish
- Ma'lumotlar bazasiga xavfsiz yozish
- CORS himoyasi

## Loyiha Tuzilishi

```
youtube-downloader/
├── src/
│   ├── models/
│   │   ├── user.py              # Asosiy ma'lumotlar bazasi modeli
│   │   └── download_log.py      # Kuzatuv modellari
│   ├── routes/
│   │   ├── user.py              # Foydalanuvchi route'lari
│   │   └── video_downloader.py  # Video yuklab olish API
│   ├── static/                  # Statik fayllar
│   ├── database/
│   │   └── app.db              # SQLite ma'lumotlar bazasi
│   └── main.py                 # Asosiy Flask ilovasi
├── venv/                       # Virtual muhit
├── requirements.txt            # Python kutubxonalari
└── README.md                   # Loyiha hujjati

youtube-downloader-frontend/
├── src/
│   ├── components/
│   │   └── ui/                 # UI komponentlari
│   ├── assets/                 # Statik resurslar
│   ├── App.jsx                 # Asosiy React komponenti
│   ├── App.css                 # Stillar
│   └── main.jsx               # Entry point
├── public/                     # Ommaviy fayllar
├── package.json               # Node.js kutubxonalari
└── vite.config.js             # Vite konfiguratsiyasi
```

## O'rnatish va Ishga Tushirish

### Backend (Flask)
```bash
cd youtube-downloader
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
Server http://localhost:5001 da ishga tushadi.

### Frontend (React)
```bash
cd youtube-downloader-frontend
npm install
npm run dev
```
Frontend http://localhost:5174 da ishga tushadi.

## API Hujjatlari

### Video Ma'lumotlarini Olish
**POST** `/api/get_video_info`

**So'rov:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Javob:**
```json
{
  "success": true,
  "data": {
    "title": "Video sarlavhasi",
    "uploader": "Kanal nomi",
    "duration": "03:45",
    "thumbnail": "https://...",
    "view_count": 1000000,
    "formats": [
      {
        "format_id": "18",
        "quality": "360p",
        "ext": "mp4",
        "filesize": "10.5 MB"
      }
    ]
  }
}
```

### Video Yuklab Olish
**POST** `/api/download_video`

**So'rov:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "format_id": "18"
}
```

**Javob:** Video fayli (binary stream)

## Xususiyatlar

### ✅ Amalga oshirilgan
- YouTube video ma'lumotlarini olish
- Turli formatlar va sifatlarda yuklab olish
- Responsive va interaktiv dizayn
- Ma'lumotlar bazasi kuzatuvi
- Xatoliklarni boshqarish
- CORS qo'llab-quvvatlash

### 🔄 Kelajakda qo'shilishi mumkin
- Instagram qo'llab-quvvatlash
- Foydalanuvchi ro'yxatdan o'tish tizimi
- Yuklab olish tarixi
- Admin panel
- Reklama integratsiyasi
- Bulk yuklab olish

## Texnik Talablar

### Server Talablari
- Python 3.11+
- 1GB RAM (minimal)
- 10GB disk maydoni
- Internet aloqasi

### Brauzer Qo'llab-quvvatlash
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Litsenziya va Huquqiy Jihatlar

⚠️ **Muhim eslatma**: Bu veb-sayt faqat ta'lim va shaxsiy foydalanish maqsadlarida yaratilgan. YouTube'ning xizmat ko'rsatish shartlariga muvofiq, mualliflik huquqi bilan himoyalangan kontentni ruxsatsiz yuklab olish va tarqatish taqiqlanadi.

Foydalanuvchilar:
- Faqat o'zlariga tegishli yoki ochiq litsenziyali videolarni yuklab olishlari kerak
- Mualliflik huquqlarini hurmat qilishlari shart
- Tijorat maqsadlarida foydalanish taqiqlanadi

