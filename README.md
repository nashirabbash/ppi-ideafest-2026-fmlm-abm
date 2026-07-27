# Paratransit FMLM Agent-Based Simulation 🚍🚄

Repositori ini berisi *source code* simulasi *Agent-Based Model* (ABM) menggunakan Python `Mesa` untuk menganalisis integrasi *First-Mile/Last-Mile* (FMLM) antara angkutan paratransit (*feeder*) peri-urban dengan jaringan kereta komuter. 

Simulasi ini dikembangkan sebagai bagian dari penelitian Karya Tulis Ilmiah (KTI) untuk kompetisi **PPI IDEAFEST 2026** oleh Tim Peneliti Politeknik Perkeretaapian Indonesia Madiun.

## 🔬 Latar Belakang & Fitur Simulasi
Simulasi ini memodelkan dinamika keputusan pengemudi angkutan *feeder* (paratransit) di kawasan peri-urban menggunakan kerangka *Random Utility Maximization* (RUM). Sistem menguji skema **Integrated Real-Time Flexible Dispatch & Performance-Weighted Micro-Equity Framework** untuk mencapai stabilitas *headway* dan memangkas kelebihan waktu tunggu penumpang (*Excess Waiting Time*).

Fitur utama dalam simulasi:
- **Pulsed Arrivals**: Memodelkan gelombang kedatangan komuter dari stasiun KRL.
- **RUM Driver Agents**: Agen pengemudi mengambil keputusan rasional berdasarkan jaminan pendapatan (*Net-BOK Floor*), dividen (*Micro-Equity*), dan penalti durasi henti (*Anti-gaming penalty*).
- **Monte Carlo Runs**: Mendukung eksekusi massal skenario dengan random seed tetap (100% *reproducible*).

## 📂 Struktur Repositori

- `config.py`: Parameter jaringan spasial (koridor 8,5 km, 12 halte) dan 4 matriks *Treatment Arms*.
- `agents.py`: Implementasi logika kelas `DriverAgent` dan `PassengerAgent`.
- `model.py`: Pengelola siklus simulasi spasial-temporal menggunakan framework `Mesa`.
- `run_simulation.py`: Skrip pemicu (*entry-point*) untuk eksekusi 500 *Monte Carlo runs* dan uji hipotesis statistik otomatis.
- `plots/`: Direktori *output* untuk visualisasi hasil dan grafik distribusi (Kruskal-Wallis & ANOVA).

## 🚀 Cara Menjalankan Simulasi

### 1. Prasyarat (Dependencies)
Pastikan Anda menggunakan Python 3.9+ dan menginstal dependensi berikut:
```bash
pip install mesa numpy pandas matplotlib scipy seaborn
```

### 2. Menjalankan Model
Untuk menjalankan 500 eksperimen *Monte Carlo* secara keseluruhan beserta kalkulasi uji statistiknya, eksekusi skrip utama:
```bash
python run_simulation.py
```

Skrip ini akan secara otomatis:
1. Mengeksekusi keempat *Treatment Arms* (Masing-masing 125 *runs*).
2. Mengekspor metrik luaran (MOE) ke terminal.
3. Menyimpan visualisasi keandalan *headway*, *Excess Waiting Time* (EWT), sensitivitas anti-gaming, retensi agen, dan *Farebox Recovery Ratio* (FRR) di dalam direktori `plots/`.

## 📊 Hasil Uji (Treatment Arms)
Model ini secara komparatif menguji 4 skenario tata kelola *feeder*:
- **Arm A**: *Baseline Setoran Tradisi* (Jadwal kaku, tanpa insentif, risiko "ngetem").
- **Arm B**: *Flat Wage* (Gaji harian datar, tanpa syarat KPI keselamatan & headway).
- **Arm C**: *Unprotected Flexible Dispatch* (Jadwal adaptif, tanpa jaminan perlindungan pendapatan).
- **Arm D**: *UNIFIED FRAMEWORK* (Solusi Usulan: Jadwal adaptif, *Net-BOK Floor*, 15% *Micro-Equity*, penalti telemetri).

Skenario **Arm D** divalidasi mampu menstabilkan $CV_{\text{headway}} \le 0,18$ dan menurunkan kelebihan waktu tunggu sebesar 60,35% dibandingkan *baseline*.

## 📜 Lisensi
Dikembangkan untuk keperluan kompetisi inovasi akademis PPI IDEAFEST 2026. Data dan simulasi ini dirilis secara terbuka untuk mendorong replikasi ilmiah (*Open Science*).
