# 🇦🇿 Azərbaycan Satış Analizi Dashboard

**Junior Data Analyst Portfolio Project**

Real Azərbaycan satış datası üzərində end-to-end layihə:

**CSV → Python (təmizləmə) → SQLite + SQL sorğuları → Streamlit Dashboard**

---

## Dataset

| Göstərici | Dəyər |
|-----------|-------|
| Sifariş sayı | 500 |
| Dövr | 2024 – 2025 |
| Regionlar | Bakı, Gəncə, Sumqayıt, Mingəçevir, Şəki |
| Kateqoriyalar | Elektronika, Ev əşyaları, Geyim, İdman, Kitab |
| Satış nümayəndələri | Aysel, Elvin, Kamran, Ləman, Nigar, Rəşad |

---

## Layihə strukturu

```
azerbaijan-sales-analysis/
├── data/
│   ├── sales_data.csv          # Orijinal data
│   └── sales.db                # SQLite (script ilə yaranır)
├── scripts/
│   └── load_to_sqlite.py       # CSV → SQLite pipeline
├── sql/
│   ├── analysis_queries.sql           # Orijinal SQL
│   └── analysis_queries_sqlite.sql    # SQLite uyğun versiya
├── dashboard/
│   └── app.py                  # Streamlit interaktiv dashboard
├── requirements.txt
└── README.md
```

---

## İşə salmaq

```bash
pip install -r requirements.txt
python scripts/load_to_sqlite.py
streamlit run dashboard/app.py
```

---

## SQL sorğuları (12 ədəd)

1. Ümumi KPI-lər  
2. Region üzrə satış  
3. Kateqoriya üzrə satış  
4. Satış nümayəndəsi performansı  
5. Aylıq trend  
6. Top 10 məhsul  
7. Top 10 müştəri  
8. Endirim analizi  
9. Hər regionda #1 məhsul (Window Function)  
10. Kumulativ satış (Running Total)  
11. YoY müqayisə (2024 vs 2025)  
12. Müştəri seqmenti (VIP / Yüksək / Orta / Aşağı)

---

## Skills

- **Python / Pandas** – data loading & feature engineering  
- **SQL** – aggregations, CTE, Window Functions, CASE  
- **SQLite** – local database  
- **Streamlit + Plotly** – interaktiv dashboard  
- **Business analysis** – region, salesperson, discount, customer segments
