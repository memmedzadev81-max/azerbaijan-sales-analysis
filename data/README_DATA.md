# Data

`sales_data.csv` faylını full versiyada yükləmək üçün:

1. Orijinal `sales__data.csv` faylını (500 sətir) bu qovluğa `sales_data.csv` adı ilə kopyalayın
2. Və ya layihəni clone edib local-da öz CSV-nizi qoyun

Sonra:
```bash
python scripts/load_to_sqlite.py
streamlit run dashboard/app.py
```

**Qeyd:** Repo-da nümunə CSV var. Tam 500 sətirlik data üçün öz faylınızı əlavə edin.
