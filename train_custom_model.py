"""
Train the BEST model using YOUR custom dataset
Maximum accuracy - no time/hardware limits
"""

import numpy as np
import os
import json
from datetime import datetime
import shutil
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

class CustomModelTrainer:
    def __init__(self):
        self.dataset_dir = "my_custom_dataset"
        self.landmarks_dir = os.path.join(self.dataset_dir, "landmarks")
        self.model_dir = "models"
        self.backup_dir = "model_backups"
        
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Classes (28 + nothing handled at detection level)
        self.classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                       'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                       'space', 'del']
    
    def load_custom_dataset(self):
        """Load YOUR custom dataset"""
        print("\n📂 Loading YOUR custom dataset...")
        
        sequences = []
        labels = []
        
        for class_idx, class_name in enumerate(self.classes):
            class_dir = os.path.join(self.landmarks_dir, class_name)
            
            if not os.path.exists(class_dir):
                print(f"  ⚠️  No data for {class_name}")
                continue
            
            landmark_files = [f for f in os.listdir(class_dir) if f.endswith('.npy')]
            
            for landmark_file in landmark_files:
                filepath = os.path.join(class_dir, landmark_file)
                landmarks = np.load(filepath)
                sequences.append(landmarks)
                labels.append(class_idx)
            
            print(f"  ✅ {class_name}: {len(landmark_files)} samples")
        
        sequences = np.array(sequences)
        labels = np.array(labels)
        
        print(f"\n✅ Loaded {len(sequences)} total samples")
        print(f"   Feature shape: {sequences.shape}")
        print(f"   Classes: {len(self.classes)}")
        
        return sequences, labels
    
    def augment_data(self, sequences, labels, augmentation_factor=3):
        """Augment data for better generalization"""
        print(f"\n🔄 Augmenting data ({augmentation_factor}x)...")
        
        augmented_sequences = [sequences]
        augmented_labels = [labels]
        
        for i in range(augmentation_factor - 1):
            # Add random noise
            noise = np.random.normal(0, 0.01, sequences.shape)
            noisy_data = sequences + noise
            
            # Random scaling
            scale = np.random.uniform(0.95, 1.05, (sequences.shape[0], 1))
            scaled_data = sequences * scale
            
            augmented_sequences.append(noisy_data)
            augmented_sequences.append(scaled_data)
            augmented_labels.append(labels)
            augmented_labels.append(labels)
        
        final_sequences = np.vstack(augmented_sequences)
        final_labels = np.hstack(augmented_labels)
        
        print(f"✅ Augmented: {len(sequences)} → {len(final_sequences)} samples")
        
        return final_sequences, final_labels
    
    def create_advanced_model(self, input_shape, num_classes):
        """Create advanced CNN architecture for maximum accuracy"""
        print("\n🔨 Building ADVANCED model architecture...")
        
        model = keras.Sequential([
            # Input
            keras.layers.Input(shape=input_shape),
            keras.layers.Reshape((input_shape[0], 1)),
            
            # Block 1
            keras.layers.Conv1D(128, 5, activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv1D(128, 5, activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling1D(2),
            keras.layers.Dropout(0.2),
            
            # Block 2
            keras.layers.Conv1D(256, 5, activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv1D(256, 5, activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling1D(2),
            keras.layers.Dropout(0.3),
            
            # Block 3
            keras.layers.Conv1D(512, 3, activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv1D(512, 3, activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.GlobalAveragePooling1D(),
            keras.layers.Dropout(0.4),
            
            # Dense layers
            keras.layers.Dense(1024, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),
            
            keras.layers.Dense(512, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),
            
            keras.layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),
            
            # Output
            keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        print("✅ Model architecture created")
        model.summary()
        
        return model
    
    def train_model(self, sequences, labels):
        """Train the model with best practices"""
        print("\n" + "="*70)
        print("  TRAINING BEST MODEL")
        print("="*70)
        
        # Normalize data
        print("\n📊 Normalizing data...")
        scaler = StandardScaler()
        sequences_normalized = scaler.fit_transform(sequences)
        
        # Save scaler
        scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        print(f"💾 Scaler saved: {scaler_path}")
        
        # Split data
        print("\n📊 Splitting data...")
        X_train, X_temp, y_train, y_temp = train_test_split(
            sequences_normalized, labels,
            test_size=0.3, random_state=42, stratify=labels
        )
        
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp,
            test_size=0.5, random_state=42, stratify=y_temp
        )
        
        print(f"   Training: {len(X_train)} samples")
        print(f"   Validation: {len(X_val)} samples")
        print(f"   Test: {len(X_test)} samples")
        
        # Create model
        model = self.create_advanced_model((sequences.shape[1],), len(self.classes))
        
        # Compile
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        )
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=20,
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=7,
                min_lr=1e-7,
                verbose=1
            ),
            keras.callbacks.ModelCheckpoint(
                os.path.join(self.model_dir, 'best_custom_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            keras.callbacks.CSVLogger(
                os.path.join(self.model_dir, 'training_history.csv')
            )
        ]
        
        # Train
        print("\n🚀 Starting training...")
        print("⏰ This may take 1-3 hours for maximum accuracy")
        print("="*70 + "\n")
        
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=100,  # Maximum epochs
            batch_size=16,  # Smaller batch for better gradients
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate
        print("\n📊 Final Evaluation:")
        train_results = model.evaluate(X_train, y_train, verbose=0)
        val_results = model.evaluate(X_val, y_val, verbose=0)
        test_results = model.evaluate(X_test, y_test, verbose=0)
        
        print(f"\n   Training:")
        print(f"      Accuracy: {train_results[1]*100:.2f}%")
        print(f"      Top-3 Accuracy: {train_results[2]*100:.2f}%")
        
        print(f"\n   Validation:")
        print(f"      Accuracy: {val_results[1]*100:.2f}%")
        print(f"      Top-3 Accuracy: {val_results[2]*100:.2f}%")
        
        print(f"\n   Test:")
        print(f"      Accuracy: {test_results[1]*100:.2f}%")
        print(f"      Top-3 Accuracy: {test_results[2]*100:.2f}%")
        
        # Save final model
        model_path = os.path.join(self.model_dir, 'signity_custom_model.h5')
        model.save(model_path)
        print(f"\n💾 Model saved: {model_path}")
        
        # Save class mapping
        class_mapping = {
            'model_to_class': {str(i): self.classes[i] for i in range(len(self.classes))},
            'original_indices': list(range(len(self.classes))),
            'num_classes': len(self.classes)
        }
        
        mapping_path = os.path.join(self.model_dir, 'custom_class_mapping.json')
        with open(mapping_path, 'w') as f:
            json.dump(class_mapping, f, indent=2)
        print(f"💾 Class mapping saved: {mapping_path}")
        
        # Create backup
        self.create_model_backup(model_path, test_results[1])
        
        return model, history, test_results[1]
    
    def create_model_backup(self, model_path, accuracy):
        """Create timestamped backup of trained model"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        accuracy_str = f"{accuracy*100:.2f}".replace('.', '_')
        backup_name = f"model_acc{accuracy_str}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy model
        shutil.copy(model_path, os.path.join(backup_path, 'model.h5'))
        
        # Copy scaler
        scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
        if os.path.exists(scaler_path):
            shutil.copy(scaler_path, os.path.join(backup_path, 'scaler.pkl'))
        
        # Copy class mapping
        mapping_path = os.path.join(self.model_dir, 'custom_class_mapping.json')
        if os.path.exists(mapping_path):
            shutil.copy(mapping_path, os.path.join(backup_path, 'class_mapping.json'))
        
        # Create info file
        info_path = os.path.join(backup_path, 'model_info.txt')
        with open(info_path, 'w') as f:
            f.write(f"Model Backup\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Test Accuracy: {accuracy*100:.2f}%\n")
            f.write(f"Classes: {len(self.classes)}\n")
        
        print(f"💾 Model backup created: {backup_path}")
    
    def run_full_training(self):
        """Complete training pipeline"""
        print("\n" + "="*70)
        print("  CUSTOM MODEL TRAINING")
        print("="*70)
        print("\nThis will train the BEST model using YOUR dataset:")
        print("  🎯 Maximum accuracy (no time/hardware limits)")
        print("  📊 Advanced CNN architecture")
        print("  🔄 3x data augmentation")
        print("  ⏱️  Estimated time: 1-3 hours")
        print("  💾 Automatic backups")
        print("="*70)
        
        response = input("\nStart training? (y/n): ").strip().lower()
        if response != 'y':
            return
        
        # Load dataset
        sequences, labels = self.load_custom_dataset()
        
        if len(sequences) == 0:
            print("\n❌ No data found! Run create_custom_dataset.py first")
            return
        
        # Augment data
        sequences_aug, labels_aug = self.augment_data(sequences, labels, augmentation_factor=3)
        
        # Train
        model, history, accuracy = self.train_model(sequences_aug, labels_aug)
        
        print("\n" + "="*70)
        print("  ✅ TRAINING COMPLETE!")
        print("="*70)
        print(f"\n🎯 Final Test Accuracy: {accuracy*100:.2f}%")
        print(f"\n📁 Files created:")
        print(f"   - models/signity_custom_model.h5 (main model)")
        print(f"   - models/best_custom_model.h5 (best checkpoint)")
        print(f"   - models/scaler.pkl (data normalizer)")
        print(f"   - models/custom_class_mapping.json (class mapping)")
        print(f"   - model_backups/ (timestamped backups)")
        print(f"\n🚀 Next step: Test your model")
        print(f"   python sign_to_speech.py")
        print("="*70)

def main():
    trainer = CustomModelTrainer()
    trainer.run_full_training()

if __name__ == "__main__":
    main()
