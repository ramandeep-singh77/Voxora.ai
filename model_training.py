"""
Signity.AI - Model Training Module
Trains deep learning model for sign language recognition
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import class_weight
import matplotlib.pyplot as plt
from config import *
from data_preprocessing import DataPreprocessor

class SignLanguageModel:
    def __init__(self):
        self.model = None
        self.history = None
        
    def build_model(self, input_shape, num_classes, actual_num_classes=None):
        """Build hybrid CNN + Dense model for landmark classification"""
        # Use actual number of classes found in data
        output_classes = actual_num_classes if actual_num_classes else num_classes
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=input_shape),
            
            # Reshape for Conv1D
            layers.Reshape((NUM_LANDMARKS, LANDMARK_DIMS)),
            
            # Conv1D layers for spatial feature extraction
            layers.Conv1D(64, 3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Conv1D(128, 3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(2),
            layers.Dropout(0.3),
            
            layers.Conv1D(256, 3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling1D(),
            
            # Dense layers
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            
            # Output layer
            layers.Dense(output_classes, activation='softmax')
        ])
        
        return model
    
    def train(self, X_train, y_train, X_val, y_val):
        """Train the model"""
        # Remap labels to be continuous (0, 1, 2, ..., n-1)
        all_labels = np.concatenate([y_train, y_val])
        unique_labels = np.unique(all_labels)
        actual_num_classes = len(unique_labels)
        
        print(f"📊 Found {actual_num_classes} classes in training data")
        print(f"   Label range: {unique_labels.min()} to {unique_labels.max()}")
        
        # Create label mapping
        label_mapping = {old_label: new_label for new_label, old_label in enumerate(unique_labels)}
        
        # Remap labels
        y_train = np.array([label_mapping[label] for label in y_train])
        y_val = np.array([label_mapping[label] for label in y_val])
        
        print(f"   Remapped to: 0 to {actual_num_classes-1}")
        
        print("🏗️  Building model architecture...")
        self.model = self.build_model(
            input_shape=(NUM_LANDMARKS * LANDMARK_DIMS,),
            num_classes=NUM_CLASSES,
            actual_num_classes=actual_num_classes
        )
        
        # Compile model
        optimizer = keras.optimizers.Adam(learning_rate=LEARNING_RATE)
        self.model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(self.model.summary())
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=EARLY_STOPPING_PATIENCE,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=REDUCE_LR_PATIENCE,
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                os.path.join(MODEL_DIR, 'best_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Calculate class weights for imbalanced data
        class_weights = class_weight.compute_class_weight(
            'balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        class_weights_dict = dict(enumerate(class_weights))
        
        print("\n🚀 Starting training...")
        print(f"⏰ This will take approximately {EPOCHS * 0.5:.0f}-{EPOCHS * 1:.0f} minutes")
        print(f"📊 Training for {EPOCHS} epochs...")
        print("⚠️  DO NOT CLOSE THIS WINDOW - Let it complete all epochs!\n")
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=callbacks,
            class_weight=class_weights_dict,
            verbose=1
        )
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print("="*60)
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\n📊 Test Results:")
        print(f"   Loss: {loss:.4f}")
        print(f"   Accuracy: {accuracy*100:.2f}%")
        return loss, accuracy
    
    def save_model(self, filename='signity_model.h5'):
        """Save trained model"""
        model_path = os.path.join(MODEL_DIR, filename)
        self.model.save(model_path)
        print(f"💾 Model saved to {model_path}")
    
    def load_model(self, filename='signity_model.h5'):
        """Load trained model"""
        model_path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(model_path):
            self.model = keras.models.load_model(model_path)
            print(f"📂 Model loaded from {model_path}")
            return True
        return False
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("⚠️  No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Accuracy plot
        ax1.plot(self.history.history['accuracy'], label='Train Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Val Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(self.history.history['loss'], label='Train Loss')
        ax2.plot(self.history.history['val_loss'], label='Val Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(MODEL_DIR, 'training_history.png'))
        print(f"📈 Training plots saved to {MODEL_DIR}/training_history.png")
        plt.show()

def main():
    """Main training pipeline"""
    # Load preprocessed data
    preprocessor = DataPreprocessor()
    sequences, labels = preprocessor.load_processed_data('train')
    
    if sequences is None:
        print("❌ No processed data found. Run data_preprocessing.py first!")
        return
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        sequences, labels,
        test_size=0.15,
        random_state=42,
        stratify=labels
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train,
        test_size=0.15,
        random_state=42,
        stratify=y_train
    )
    
    print(f"📊 Data Split:")
    print(f"   Train: {len(X_train)} samples")
    print(f"   Val: {len(X_val)} samples")
    print(f"   Test: {len(X_test)} samples")
    
    # Train model
    model = SignLanguageModel()
    model.train(X_train, y_train, X_val, y_val)
    
    # Evaluate
    model.evaluate(X_test, y_test)
    
    # Save model
    model.save_model()
    
    # Plot history
    model.plot_training_history()

if __name__ == "__main__":
    main()
