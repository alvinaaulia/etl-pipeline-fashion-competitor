# etl-pipeline-fashion-competitor
etl-pipeline-fashion-competitor adalah proyek end-to-end yang dirancang untuk mengotomatisasi proses ekstraksi, transformasi, dan pemuatan (ETL) data kompetitor di industri fashion. Proyek ini menargetkan data dari situs kompetitor fashion online untuk dianalisis lebih lanjut dalam mendukung pengambilan keputusan bisnis berbasis data.

Pipeline ini dikembangkan menggunakan Python dengan berbagai pustaka seperti BeautifulSoup, Requests, Pandas, dan SQLAlchemy, serta didukung oleh database PostgreSQL/MySQL untuk penyimpanan data terstruktur. Proses ETL mencakup tiga tahap utama:
- Extract: Mengambil data produk (nama, harga, kategori, dan rating) dari situs web kompetitor menggunakan teknik web scraping.
- Transform: Membersihkan dan mengubah data mentah menjadi format yang konsisten dan siap dianalisis (misalnya, konversi harga, standarisasi nama kategori, penghapusan duplikasi).
- Load: Memasukkan data yang sudah dibersihkan ke dalam database relasional untuk analisis lebih lanjut dan integrasi ke dalam dashboard atau sistem intelijen bisnis.

### Fitur unggulan:
- Modular dan mudah dikonfigurasi untuk berbagai sumber data.
- Logging terintegrasi untuk monitoring dan debugging.
- Dirancang untuk skalabilitas dalam penggunaan pada banyak situs kompetitor.

Cocok digunakan oleh analis data, business intelligence engineer, atau tim pemasaran digital yang ingin melacak perubahan produk dan harga dari kompetitor secara periodik dan otomatis.

### Struktur Direktori:
```
├── utils/
│   ├── load.py
│   ├── extract.py
│   ├── transform.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py 
│   └── test_load.py
│
├── .coverage
├── main.py
├── etl-fashion-460408-6eb71c372cbb.json
├── products.csv
├── submission.txt
└── test_products.csv
```

🔧 Teknologi:
Python, BeautifulSoup, Pandas, SQLAlchemy, PostgreSQL.

