# TINote — pengumuman kelas santai

MVT Django + Tailwind CDN + DaisyUI + Postgres (Supabase).

## Jalanin lokal (sqlite, tanpa Supabase dulu)
```bash
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser  # isi NIM, nama, PIN 6 digit (misal 123456)
python manage.py runserver
```
Buka http://127.0.0.1:8000/login/

## Pakai Supabase Postgres
1. Di Supabase → Project Settings → Database → ambil Pooling connection string (port 6543).
2. Isi `.env`: `DATABASE_URL=postgresql://...?sslmode=require`
3. `python manage.py migrate` terus `runserver` lagi.

## Akun & role
- Semua wajib login. Belum login dilempar ke `/login/`.
- Login: NIM + PIN 6 digit + centang "Ingat saya 3 hari".
- Role `staff` bisa: kelola user (tambah 1-1 / import CSV `NIM,Nama,Role,PIN`, edit role, reset PIN random, hapus), CRUD matkul, CRUD pengumuman, hapus komentar siapa pun.
- Role `mahasiswa`: lihat dashboard, filter matkul, search, sort deadline terdekat/terjauh, komentar, tandai selesai (kesimpan per user).
- Ganti PIN sendiri di menu. Lupa PIN minta reset ke staff.

## Matkul
Kode, nama, dosen, hari, jam mulai–selesai, ruang. Tampil di card dashboard + halaman matkul.

## Catatan
- Timezone `Asia/Jakarta`, bahasa santai.
- Tema neo-brutalism + Space Mono, toggle gelap/terang, responsive.
