# main.py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import tempfile

print("TensorFlow version:", tf.__version__)

# ================= CELL 2: Set Variables =================
# Cari folder cats_and_dogs secara otomatis
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Coba beberapa lokasi yang mungkin
possible_paths = [
    os.path.join(current_dir, 'cats_and_dogs'),  # Satu folder dengan script
    os.path.join(current_dir, '..', 'cats_and_dogs'),  # Di parent folder
    os.path.join(current_dir, '..', '..', 'cats_and_dogs'),  # Di parent of parent
    'cats_and_dogs',  # Di current working directory
]

PATH = None
for path in possible_paths:
    if os.path.exists(path):
        PATH = path
        print(f"Found dataset at: {PATH}")
        break

if PATH is None:
    print("ERROR: Folder 'cats_and_dogs' tidak ditemukan!")
    print("Pastikan struktur folder seperti ini:")
    print("Project/")
    print("├── src/")
    print("│   └── main.py")
    print("└── cats_and_dogs/")
    print("    ├── train/")
    print("    │   ├── cats/")
    print("    │   └── dogs/")
    print("    ├── validation/")
    print("    │   ├── cats/")
    print("    │   └── dogs/")
    print("    └── test/")
    exit()

# Set paths dengan pengecekan
train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

print(f"\nTrain directory exists: {os.path.exists(train_dir)}")
print(f"Validation directory exists: {os.path.exists(validation_dir)}")
print(f"Test directory exists: {os.path.exists(test_dir)}")

# Jika ada folder yang tidak ditemukan, coba alternatif
if not os.path.exists(train_dir):
    # Coba cek isi PATH langsung
    print(f"\nChecking contents of {PATH}:")
    for item in os.listdir(PATH):
        item_path = os.path.join(PATH, item)
        if os.path.isdir(item_path):
            print(f"  {item}/")
            # Cek isi subfolder
            for subitem in os.listdir(item_path)[:3]:
                print(f"    {subitem}")

BATCH_SIZE = 128
IMG_HEIGHT = 150
IMG_WIDTH = 150

# ================= CELL 3: Create Image Generators =================
print("\n=== Creating Image Generators ===")

# 1. TRAIN Generator
print("\n1. Creating TRAIN generator...")
try:
    train_image_generator = ImageDataGenerator(rescale=1./255)
    train_data_gen = train_image_generator.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        class_mode='binary'
    )
    print(f"✓ Train generator created: {train_data_gen.samples} images, {train_data_gen.num_classes} classes")
except Exception as e:
    print(f"✗ Error creating train generator: {e}")
    exit()

# 2. VALIDATION Generator
print("\n2. Creating VALIDATION generator...")
try:
    validation_image_generator = ImageDataGenerator(rescale=1./255)
    val_data_gen = validation_image_generator.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=validation_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        class_mode='binary'
    )
    print(f"✓ Validation generator created: {val_data_gen.samples} images, {val_data_gen.num_classes} classes")
except Exception as e:
    print(f"✗ Error creating validation generator: {e}")
    exit()

# 3. TEST Generator (Special handling)
print("\n3. Creating TEST generator...")

# Cek isi test directory
if not os.path.exists(test_dir):
    print(f"✗ Test directory not found: {test_dir}")
    print("Creating empty test generator...")
    # Buat dummy test generator
    class DummyTestGenerator:
        def __init__(self):
            self.samples = 50
            self.batch_size = 1
            self.index = 0
            
        def __len__(self):
            return 50
            
        def reset(self):
            self.index = 0
            
        def __next__(self):
            if self.index >= 50:
                self.reset()
                raise StopIteration
            # Return dummy black image
            dummy_img = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3))
            self.index += 1
            return np.array([dummy_img])
    
    test_data_gen = DummyTestGenerator()
else:
    # Ada test directory
    test_files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(test_files)} images in test directory")
    
    if len(test_files) > 0:
        # Buat temporary directory untuk test (karena flow_from_directory butuh subdirectory)
        temp_dir = tempfile.mkdtemp()
        test_temp_dir = os.path.join(temp_dir, 'test')
        os.makedirs(test_temp_dir, exist_ok=True)
        
        # Copy semua test images ke temporary directory
        for file in test_files[:50]:  # Maksimal 50 sesuai requirement
            src = os.path.join(test_dir, file)
            dst = os.path.join(test_temp_dir, file)
            shutil.copy(src, dst)
        
        # Buat generator
        test_image_generator = ImageDataGenerator(rescale=1./255)
        test_data_gen = test_image_generator.flow_from_directory(
            batch_size=1,  # SESUAI: batch_size=1 untuk prediksi per image
            directory=temp_dir,
            target_size=(IMG_HEIGHT, IMG_WIDTH),
            class_mode=None,  # Tidak ada label
            shuffle=False  # SESUAI INSTRUKSI: shuffle=False
        )
        print(f"✓ Test generator created: {len(test_files)} images")
    else:
        print("✗ No images found in test directory")
        # Buat dummy seperti di atas
        test_data_gen = DummyTestGenerator()

# ================= CELL 4: Plot Images Function =================
def plotImages(images_arr, probabilities=None):
    num_images = len(images_arr)
    fig, axes = plt.subplots(num_images, 1, figsize=(6, num_images * 2.5))
    
    if num_images == 1:
        axes = [axes]
    
    for idx, img in enumerate(images_arr):
        ax = axes[idx]
        ax.imshow(img)
        ax.axis('off')
        
        if probabilities is not None:
            prob = probabilities[idx]
            if hasattr(prob, '__len__'):
                prob = prob[0] if len(prob) > 0 else 0.5
            
            if prob > 0.5:
                label = f"Dog {prob*100:.1f}%"
                color = 'red'
            else:
                label = f"Cat {(1-prob)*100:.1f}%"
                color = 'blue'
            
            ax.set_title(label, color=color, fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

# Plot 5 training images
print("\n=== Plotting 5 Training Images ===")
sample_images, sample_labels = next(train_data_gen)
plotImages(sample_images[:5])

# ================= CELL 5: Data Augmentation =================
print("\n=== Setting up Data Augmentation ===")
train_image_generator = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,           # 1. Rotation
    width_shift_range=0.2,      # 2. Width shift
    height_shift_range=0.2,     # 3. Height shift
    shear_range=0.2,            # 4. Shear
    zoom_range=0.2,             # 5. Zoom
    horizontal_flip=True,       # 6. Horizontal flip
    fill_mode='nearest'
)
print("✓ Added 6 random transformations as required")

# ================= CELL 6: Plot Augmented Images =================
print("\n=== Plotting Augmented Images ===")
train_data_gen = train_image_generator.flow_from_directory(
    batch_size=BATCH_SIZE,
    directory=train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    class_mode='binary'
)

# Get 5 augmented images
augmented_images = []
for i in range(5):
    img_batch, _ = next(train_data_gen)
    augmented_images.append(img_batch[0])

plotImages(augmented_images)

# ================= CELL 7: Create Model =================
print("\n=== Creating Neural Network Model ===")
model = Sequential([
    # Layer 1
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(2, 2),
    
    # Layer 2
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    # Layer 3
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    # Layer 4
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    # Fully connected layers
    Flatten(),
    Dense(512, activation='relu'),  # SESUAI: ReLU activation
    Dense(1, activation='sigmoid')   # Binary classification
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Model summary:")
model.summary()

# ================= CELL 8: Train Model =================
print("\n=== Training Model ===")
EPOCHS = 15

# Hitung steps (sesuai dataset FreeCodeCamp)
steps_per_epoch = 2000 // BATCH_SIZE  # 2000 training images
validation_steps = 1000 // BATCH_SIZE  # 1000 validation images

print(f"Training for {EPOCHS} epochs")
print(f"Steps per epoch: {steps_per_epoch}")
print(f"Validation steps: {validation_steps}")

history = model.fit(
    train_data_gen,
    steps_per_epoch=steps_per_epoch,
    epochs=EPOCHS,
    validation_data=val_data_gen,
    validation_steps=validation_steps,
    verbose=1
)

# ================= CELL 9: Plot Training History =================
print("\n=== Plotting Training History ===")
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(EPOCHS)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot accuracy
ax1.plot(epochs_range, acc, 'b-', label='Training Accuracy', linewidth=2)
ax1.plot(epochs_range, val_acc, 'r-', label='Validation Accuracy', linewidth=2)
ax1.set_title('Training and Validation Accuracy', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epochs')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot loss
ax2.plot(epochs_range, loss, 'b-', label='Training Loss', linewidth=2)
ax2.plot(epochs_range, val_loss, 'r-', label='Validation Loss', linewidth=2)
ax2.set_title('Training and Validation Loss', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epochs')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ================= CELL 10: Make Predictions =================
print("\n=== Making Predictions on Test Images ===")

# Reset test generator jika punya method reset
if hasattr(test_data_gen, 'reset'):
    test_data_gen.reset()

# Buat prediksi
predictions = []
test_images = []

try:
    if hasattr(test_data_gen, '__len__'):
        # Untuk generator biasa
        predictions = model.predict(test_data_gen, verbose=1)
        
        # Get test images for plotting
        if hasattr(test_data_gen, 'reset'):
            test_data_gen.reset()
            for i in range(min(50, len(test_data_gen))):
                batch = next(test_data_gen)
                test_images.append(batch[0])
    else:
        # Untuk custom generator
        for i in range(50):
            batch = next(test_data_gen)
            pred = model.predict(batch, verbose=0)
            predictions.append(pred[0][0])
            test_images.append(batch[0])
    
    print(f"Made {len(predictions)} predictions")
    
    # Plot predictions (maksimal 10 gambar untuk hemat space)
    num_to_plot = min(10, len(test_images), len(predictions))
    if num_to_plot > 0:
        print(f"Plotting {num_to_plot} predictions...")
        plotImages(test_images[:num_to_plot], predictions[:num_to_plot])
    else:
        print("No test images to plot")
        
except Exception as e:
    print(f"Error during prediction: {e}")

# ================= CELL 11: Evaluate Results =================
print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)

final_val_acc = history.history['val_accuracy'][-1]
final_train_acc = history.history['accuracy'][-1]

print(f"Final Training Accuracy:   {final_train_acc*100:.2f}%")
print(f"Final Validation Accuracy: {final_val_acc*100:.2f}%")

print("\n" + "="*60)
print("CHALLENGE RESULTS")
print("="*60)

if final_val_acc >= 0.7:
    print("🎉🎉 CONGRATULATIONS! 🎉🎉")
    print("You passed the challenge with 70%+ accuracy!")
    print("⭐⭐⭐ EXTRA CREDIT ACHIEVED! ⭐⭐⭐")
elif final_val_acc >= 0.63:
    print("✅ CONGRATULATIONS!")
    print("You passed the challenge with 63%+ accuracy!")
    print("Project requirement met!")
else:
    print("❌ KEEP TRYING!")
    print(f"You need at least 63% accuracy (current: {final_val_acc*100:.2f}%)")
    print("\nSuggestions:")
    print("1. Increase EPOCHS to 20-25")
    print("2. Add more Conv2D layers (e.g., 256 filters)")
    print("3. Add Dropout(0.5) before Dense layer")
    print("4. Use data augmentation more aggressively")

print("\n" + "="*60)

# Save model
model.save('cat_dog_classifier_fcc.h5')
print("Model saved as 'cat_dog_classifier_fcc.h5'")

# Bersihkan temporary directory jika ada
if 'temp_dir' in locals() and os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
    print("Temporary files cleaned up")