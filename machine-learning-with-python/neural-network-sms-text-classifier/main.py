import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import warnings
warnings.filterwarnings('ignore')

# Memuat data
try:
    # Memuat data pelatihan
    data_latih = pd.read_csv('train-data.tsv', sep='\t', header=None, names=['label', 'pesan'])
    
    # Memuat data validasi/uji
    data_uji = pd.read_csv('valid-data.tsv', sep='\t', header=None, names=['label', 'pesan'])
    
    print("Data berhasil dimuat!")
    print(f"Bentuk data pelatihan: {data_latih.shape}")
    print(f"Bentuk data uji: {data_uji.shape}")
    
except FileNotFoundError as e:
    print(f"Kesalahan saat memuat file: {e}")
    print("Pastikan 'train-data.tsv' dan 'valid-data.tsv' berada di direktori yang sama")
    print("Anda dapat mengunduhnya dari:")
    print("https://cdn.freecodecamp.org/project-data/sms/train-data.tsv")
    print("https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv")

# Fungsi pra-pemrosesan
def praproses_teks(teks):
    """Membersihkan dan memproses teks"""
    if not isinstance(teks, str):
        return ""
    
    # Mengubah ke huruf kecil
    teks = teks.lower()
    
    # Menghapus karakter khusus dan angka
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    
    # Menghapus spasi berlebih
    teks = re.sub(r'\s+', ' ', teks).strip()
    
    return teks

# Menyiapkan data
def siapkan_data(df):
    """Menyiapkan data untuk pelatihan"""
    # Membersihkan teks
    df['pesan_bersih'] = df['pesan'].apply(praproses_teks)
    
    # Mengubah label menjadi biner (ham: 0, spam: 1)
    df['label_biner'] = df['label'].map({'ham': 0, 'spam': 1})
    
    return df

# Memproses data
data_latih = siapkan_data(data_latih)
data_uji = siapkan_data(data_uji)

# Membuat pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)  # Menggunakan unigram dan bigram
    )),
    ('klasifikasi', MultinomialNB(alpha=0.1))
])

# Melatih model
print("\nMelatih model...")
X_latih = data_latih['pesan_bersih']
y_latih = data_latih['label_biner']
model.fit(X_latih, y_latih)

# Evaluasi pada data uji
print("\nMengevaluasi pada data uji...")
X_uji = data_uji['pesan_bersih']
y_uji = data_uji['label_biner']
akurasi = model.score(X_uji, y_uji)
print(f"Akurasi uji: {akurasi:.4f}")

# Metrik evaluasi tambahan
from sklearn.metrics import classification_report, confusion_matrix
y_pred = model.predict(X_uji)
print("\nLaporan Klasifikasi:")
print(classification_report(y_uji, y_pred, target_names=['ham', 'spam']))

print("\nMatriks Kebingungan:")
print(confusion_matrix(y_uji, y_pred))

# Membuat fungsi prediksi yang diperlukan
def prediksi_pesan(teks):
    """
    Memprediksi apakah pesan adalah ham atau spam
    
    Args:
        teks (str): Pesan yang akan diklasifikasikan
        
    Returns:
        list: [probabilitas_spam, label_prediksi]
    """
    # Pra-pemrosesan teks input
    teks_bersih = praproses_teks(teks)
    
    # Mendapatkan prediksi probabilitas
    probabilitas = model.predict_proba([teks_bersih])[0]
    
    # Probabilitas kedua adalah untuk spam (kelas 1)
    probabilitas_spam = probabilitas[1]
    
    # Menentukan label
    label_prediksi = "spam" if probabilitas_spam > 0.5 else "ham"
    
    return [float(probabilitas_spam), label_prediksi]

# Menguji fungsi dengan beberapa contoh
pesan_uji = [
    "Hei, apakah kita masih bertemu untuk makan siang hari ini?",
    "Selamat! Anda memenangkan iPhone gratis! Klik di sini untuk mengklaim.",
    "Paket Anda telah terkirim. Lacak pesanan Anda di situs web kami.",
    "PENTING: Rekening bank Anda telah disusupi. Klik untuk mengamankan.",
    "Bisakah Anda mengirimkan laporan saya besok pagi? Terima kasih!"
]

print("\nMenguji fungsi prediksi:")
print("-" * 60)
for msg in pesan_uji:
    prediksi = prediksi_pesan(msg)
    print(f"Pesan: {msg[:50]}...")
    print(f"Prediksi: {prediksi[1]} (probabilitas spam: {prediksi[0]:.4f})")
    print("-" * 60)

# Menyimpan model untuk penggunaan di masa depan
try:
    with open('model_klasifikasi_spam.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("\nModel disimpan sebagai 'model_klasifikasi_spam.pkl'")
except:
    print("\nModel tidak dapat disimpan")

print("\nModel siap digunakan! Gunakan fungsi prediksi_pesan() untuk mengklasifikasikan pesan.")