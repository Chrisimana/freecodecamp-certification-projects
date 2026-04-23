import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt

# Memuat dataset
try:
    # Mencoba membaca dari file lokal
    df = pd.read_csv('insurance.csv')
except:
    # Jika tidak ada file lokal, download dari URL
    import urllib.request
    url = "https://cdn.freecodecamp.org/project-data/health-costs/insurance.csv"
    df = pd.read_csv(url)
    df.to_csv('insurance.csv', index=False)  # Menyimpan untuk penggunaan selanjutnya

print("Bentuk dataset:", df.shape)
print("\nBeberapa baris pertama:")
print(df.head())
print("\nInformasi dataset:")
print(df.info())
print("\nNilai yang hilang:")
print(df.isnull().sum())

# Pra-pemrosesan data
# Mengubah kolom kategorikal menjadi numerik
kolom_kategorikal = ['sex', 'smoker', 'region']

# Membuat LabelEncoder untuk setiap kolom kategorikal
encoder_label = {}
for col in kolom_kategorikal:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoder_label[col] = le
    print(f"\nKategori {col}:", le.classes_)

# Memisahkan fitur dan target
X = df.drop('expenses', axis=1)
y = df['expenses']

# Membagi data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nUkuran set pelatihan: {X_train.shape}")
print(f"Ukuran set pengujian: {X_test.shape}")

# Normalisasi fitur
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Membuat model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[X_train.shape[1]]),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dense(1)
])

# Mengkompilasi model
model.compile(
    optimizer='adam',
    loss='mae',
    metrics=['mae', 'mse']
)

print("\nArsitektur model:")
model.summary()

# Melatih model
history = model.fit(
    X_train_scaled, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    verbose=1
)

# Evaluasi model pada set pengujian
print("\nMengevaluasi pada set pengujian...")
hasil_uji = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"MAE Pengujian: ${hasil_uji[1]:,.2f}")
print(f"MSE Pengujian: ${hasil_uji[2]:,.2f}")

# Membuat plot riwayat pelatihan
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['mae'], label='MAE Pelatihan')
plt.plot(history.history['val_mae'], label='MAE Validasi')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend()
plt.title('MAE Pelatihan dan Validasi')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Loss Pelatihan')
plt.plot(history.history['val_loss'], label='Loss Validasi')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Loss Pelatihan dan Validasi')

plt.tight_layout()
plt.show()

# Membuat prediksi
prediksi = model.predict(X_test_scaled).flatten()

# Membuat DataFrame perbandingan
df_hasil = pd.DataFrame({
    'Aktual': y_test.values,
    'Prediksi': prediksi,
    'Selisih': y_test.values - prediksi,
    'Selisih Absolut': np.abs(y_test.values - prediksi)
})

print("\nPrediksi vs Aktual (10 sampel pertama):")
print(df_hasil.head(10))

print(f"\nRata-rata Error Absolut: ${df_hasil['Selisih Absolut'].mean():,.2f}")
print(f"Error Absolut Maksimum: ${df_hasil['Selisih Absolut'].max():,.2f}")
print(f"Error Absolut Minimum: ${df_hasil['Selisih Absolut'].min():,.2f}")

# Memeriksa apakah MAE di bawah 3500
mae = df_hasil['Selisih Absolut'].mean()
print(f"\n{'='*50}")
print(f"Persyaratan MAE di bawah $3500: {'✓ LULUS' if mae < 3500 else '✗ GAGAL'}")
print(f"MAE Anda: ${mae:,.2f}")
print(f"Batas: $3,500.00")
print(f"{'='*50}")

# Membuat plot prediksi vs aktual
plt.figure(figsize=(10, 6))
plt.scatter(y_test, prediksi, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Biaya Aktual ($)')
plt.ylabel('Biaya Prediksi ($)')
plt.title('Biaya Kesehatan Aktual vs Prediksi')
plt.grid(True, alpha=0.3)

# Menambahkan statistik error ke plot
plt.text(0.05, 0.95, f'MAE: ${mae:,.2f}', 
         transform=plt.gca().transAxes, 
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()

# Membuat plot distribusi error
plt.figure(figsize=(10, 6))
plt.hist(df_hasil['Selisih'], bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Error Prediksi (Aktual - Prediksi)')
plt.ylabel('Frekuensi')
plt.title('Distribusi Error Prediksi')
plt.axvline(x=0, color='r', linestyle='--', label='Error Nol')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

# Analisis pentingnya fitur (menggunakan permutation importance)
def pentingnya_permutasi(model, X, y, metrik='mae', n_pengulangan=10):
    skor_dasar = np.mean(np.abs(y - model.predict(X).flatten()))
    kepentingan = []
    
    for i in range(X.shape[1]):
        X_permutasi = X.copy()
        skor = []
        for _ in range(n_pengulangan):
            X_permutasi[:, i] = np.random.permutation(X_permutasi[:, i])
            pred = model.predict(X_permutasi, verbose=0).flatten()
            skor_error = np.mean(np.abs(y - pred))
            skor.append(skor_error)
        
        kepentingan_fitur = np.mean(skor) - skor_dasar
        kepentingan.append(kepentingan_fitur)
    
    return kepentingan

# Menghitung pentingnya fitur
kepentingan_fitur = pentingnya_permutasi(
    model, X_test_scaled, y_test.values, n_pengulangan=5
)

# Membuat plot pentingnya fitur
fitur = X.columns
plt.figure(figsize=(10, 6))
batang = plt.barh(range(len(fitur)), kepentingan_fitur)
plt.yticks(range(len(fitur)), fitur)
plt.xlabel('Kepentingan (Peningkatan MAE saat fitur diacak)')
plt.title('Kepentingan Fitur')
plt.grid(True, alpha=0.3, axis='x')

# Mewarnai batang berdasarkan kepentingan
for bar, importance in zip(batang, kepentingan_fitur):
    if importance > 0:
        bar.set_color('red')
    else:
        bar.set_color('green')

plt.tight_layout()
plt.show()

# Pengujian dengan sampel data baru
print("\nPengujian dengan sampel baru:")
data_sampel = [
    [19, 0, 27.9, 0, 1, 3],  # muda, perempuan, BMI normal, bukan perokok, barat daya
    [45, 1, 35.5, 2, 0, 2],  # setengah baya, laki-laki, obesitas, perokok, barat laut
    [60, 1, 28.5, 0, 1, 1],  # lanjut usia, laki-laki, kelebihan berat badan, bukan perokok, tenggara
]

for i, sampel in enumerate(data_sampel):
    sampel_scaled = scaler.transform([sampel])
    prediksi = model.predict(sampel_scaled, verbose=0)[0][0]
    print(f"Sampel {i+1}: Biaya prediksi = ${prediksi:,.2f}")

# Menyimpan model
model.save('model_biaya_kesehatan.h5')
print("\nModel disimpan sebagai 'model_biaya_kesehatan.h5'")

# Menyimpan scaler dan encoder
import joblib
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(encoder_label, 'encoder_label.pkl')
print("Objek pra-pemrosesan disimpan")