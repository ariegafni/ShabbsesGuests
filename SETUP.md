# ShabbesGuests Backend Setup

## התקנה והפעלה

### 1. התקנת תלויות
```bash
pip install -r requirements.txt
```

### 2. הגדרת בסיס נתונים
1. צור בסיס נתונים PostgreSQL חדש:
```sql
CREATE DATABASE shabbes_guests;
```

2. הרץ את סקריפט הסכמה:
```bash
psql -d shabbes_guests -f schema.sql
```

### 3. הגדרת משתני סביבה
צור קובץ `.env` בהתבסס על `env_example.txt`:
```bash
cp env_example.txt .env
```

עדכן את הערכים בקובץ `.env`:
- `DB_PASS` - סיסמת PostgreSQL שלך
- `JWT_SECRET` - מפתח סודי חזק ל-JWT

### 4. הפעלת השרת
```bash
python app.py
```

השרת יפעל על `http://127.0.0.1:3002`

## Endpoints זמינים

### אותנטיקציה
- `POST /api/auth/register` - הרשמת משתמש חדש
- `POST /api/auth/login` - התחברות
- `POST /api/auth/refresh` - רענון טוקן
- `POST /api/auth/logout` - התנתקות
- `POST /api/auth/forgot-password` - שכחתי סיסמה
- `POST /api/auth/reset-password` - איפוס סיסמה
- `POST /api/auth/verify-email` - אימות אימייל

### משתמש
- `GET /api/users/me` - קבלת פרופיל המשתמש הנוכחי
- `PUT /api/users/me` - עדכון פרופיל
- `DELETE /api/users/me` - מחיקת חשבון
- `PUT /api/users/change-password` - שינוי סיסמה
- `POST /api/users/upload-profile-image` - העלאת תמונת פרופיל

### מארחים (Hosts)
- `GET /api/hosts` - רשימת כל המארחים (פומבי)
- `GET /api/hosts/country/<country_place_id>` - מארחים לפי מדינה (פומבי)
- `GET /api/hosts/<host_id>` - פרטי מארח ספציפי (פומבי)
- `GET /api/hosts/me` - פרופיל המארח של המשתמש הנוכחי (מוגן)
- `POST /api/hosts` - יצירת פרופיל מארח (מוגן)
- `PUT /api/hosts/<host_id>` - עדכון פרופיל מארח (מוגן)
- `DELETE /api/hosts/<host_id>` - מחיקת פרופיל מארח (מוגן)
- `POST /api/hosts/upload-photo` - העלאת תמונת מארח (מוגן)

### מיקומים (Locations)
- `GET /api/locations/countries` - רשימת מדינות
- `GET /api/locations/cities/country/<country_place_id>` - ערים לפי מדינה
- `GET /api/locations/search` - חיפוש מיקומים
- `GET /api/locations/reverse-geocode` - מיקום לפי קואורדינטות
- `GET /api/locations/nearby` - מיקומים קרובים
- `GET /api/locations/popular` - מיקומים פופולריים
- `GET /api/locations/autocomplete` - השלמה אוטומטית

## מבנה התגובה

### הרשמה/התחברות
```json
{
  "user": {
    "id": "uuid",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string?",
    "country": "string?",
    "city": "string?",
    "profile_image": "string?",
    "bio": "string?",
    "social_links": [],
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "Bearer"
}
```

### פרופיל מארח
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "country_place_id": "string",
  "city_place_id": "string",
  "area": "string?",
  "address": "string?",
  "description": "string?",
  "bio": "string?",
  "max_guests": 8,
  "hosting_type": ["shabbos_meal", "sleepover"],
  "kashrut_level": "string?",
  "languages": ["he", "en"],
  "total_hostings": 0,
  "is_always_available": false,
  "available": true,
  "photo_url": "string?",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## בדיקות

### בדיקת אותנטיקציה
```bash
python test_auth.py
```

### בדיקת מערכת המארחים
```bash
python test_hosts.py
```

## אבטחה

- כל הסיסמאות מוצפנות עם werkzeug
- JWT tokens עם תוקף מוגבל
- Access token: 15 דקות
- Refresh token: 7 ימים
- אימות חובה לכל endpoints מוגנים
- בדיקת הרשאות לעדכון/מחיקת פרופיל מארח
