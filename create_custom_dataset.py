"""
Signity.AI - Custom Dataset Creator
Collect YOUR own ASL dataset from camera with automatic backups
"""

import cv2
import numpy as np
import os
import time
from datetime import datetime
import shutil
from hand_detector import HandDetector

class CustomDatasetCreator:
    def __init__(self):
        self.hand_detector = HandDetector()
        
        # Dataset configuration
        self.base_dir = "my_custom_dataset"
        self.backup_dir = "dataset_backups"
        self.raw_images_dir = os.path.join(self.base_dir, "raw_images")
        self.landmarks_dir = os.path.join(self.base_dir, "landmarks")
        
        # Classes to collect
        self.classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                       'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                       'space', 'del']
        
        # Samples per class (more = better accuracy)
        self.samples_per_class = 500  # 500 samples per letter = 14,000 total
        
        # Create directories
        self.setup_directories()
        
    def setup_directories(self):
        """Create all necessary directories"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.raw_images_dir, exist_ok=True)
        os.makedirs(self.landmarks_dir, exist_ok=True)
        
        # Create class folders
        for class_name in self.classes:
            os.makedirs(os.path.join(self.raw_images_dir, class_name), exist_ok=True)
            os.makedirs(os.path.join(self.landmarks_dir, class_name), exist_ok=True)
        
        print("✅ Directory structure created")
    
    def get_asl_reference(self, letter):
        """Get ASL sign reference for each letter"""
        references = {
            'A': "Closed fist with thumb on the side",
            'B': "Flat hand, fingers together, thumb across palm",
            'C': "Curved hand like holding a cup",
            'D': "Index finger up, other fingers touch thumb",
            'E': "Closed fist, thumb across fingers",
            'F': "OK sign (thumb and index form circle)",
            'G': "Index and thumb horizontal, pointing sideways",
            'H': "Index and middle finger horizontal",
            'I': "Pinky finger up, fist closed",
            'J': "Pinky up, draw a J in the air",
            'K': "Index and middle up in V, thumb between them",
            'L': "L shape with thumb and index",
            'M': "Three fingers down over thumb",
            'N': "Two fingers down over thumb",
            'O': "Fingers and thumb form a circle",
            'P': "Like K but pointing down",
            'Q': "Like G but pointing down",
            'R': "Index and middle crossed",
            'S': "Fist with thumb wrapped around fingers",
            'T': "Thumb between index and middle",
            'U': "Index and middle up together",
            'V': "Index and middle up in V shape",
            'W': "Three fingers up (index, middle, ring)",
            'X': "Index finger bent like a hook",
            'Y': "Thumb and pinky out (hang loose)",
            'Z': "Draw a Z in the air with index finger",
            'space': "Open hand, palm facing camera",
            'del': "Closed fist moving backward"
        }
        return references.get(letter, "No reference available")
    
    def collect_class_data(self, class_name, samples_to_collect):
        """Collect data for a specific class"""
        print(f"\n{'='*70}")
        print(f"  COLLECTING: {class_name}")
        print(f"{'='*70}")
        print(f"\n📖 ASL Sign Reference:")
        print(f"   {self.get_asl_reference(class_name)}")
        print(f"\n🎯 Target: {samples_to_collect} samples")
        print(f"\n💡 Tips:")
        print(f"   - Move your hand slightly between captures")
        print(f"   - Try different angles (left, right, center)")
        print(f"   - Vary distance slightly (closer/farther)")
        print(f"   - Keep hand clearly visible")
        print(f"   - Auto-captures every 0.2 seconds")
        print(f"{'='*70}\n")
        
        input("Press ENTER when ready to start...")
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        samples_collected = 0
        last_capture_time = 0
        capture_interval = 0.2  # Capture every 0.2 seconds
        
        # Check existing samples
        existing_images = len([f for f in os.listdir(os.path.join(self.raw_images_dir, class_name)) 
                              if f.endswith('.jpg')])
        existing_landmarks = len([f for f in os.listdir(os.path.join(self.landmarks_dir, class_name)) 
                                 if f.endswith('.npy')])
        
        start_index = max(existing_images, existing_landmarks)
        
        if start_index > 0:
            print(f"📂 Found {start_index} existing samples, continuing from there...")
        
        try:
            while samples_collected < samples_to_collect:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                current_time = time.time()
                
                # Detect hand and extract landmarks
                frame_with_hand, landmarks, hand_present = self.hand_detector.detect_hand(frame)
                
                h, w = frame_with_hand.shape[:2]
                
                # Dark overlay for better text visibility
                overlay = frame_with_hand.copy()
                cv2.rectangle(overlay, (0, 0), (w, 180), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.7, frame_with_hand, 0.3, 0, frame_with_hand)
                
                # Progress bar
                progress = samples_collected / samples_to_collect
                bar_width = w - 40
                bar_height = 40
                cv2.rectangle(frame_with_hand, (20, 20), (20 + bar_width, 60), (50, 50, 50), -1)
                cv2.rectangle(frame_with_hand, (20, 20), (20 + int(bar_width * progress), 60), (0, 255, 0), -1)
                
                # Progress text
                cv2.putText(frame_with_hand, f"{samples_collected + start_index}/{samples_to_collect + start_index}", 
                           (w//2 - 60, 48), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                
                # Class name and reference
                cv2.putText(frame_with_hand, f"Letter: {class_name}", (20, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
                cv2.putText(frame_with_hand, self.get_asl_reference(class_name)[:50], (20, 140),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                # Hand status and auto-capture
                if hand_present and landmarks is not None:
                    if current_time - last_capture_time > capture_interval:
                        # Save raw image
                        img_filename = f"{class_name}_{start_index + samples_collected:04d}.jpg"
                        img_path = os.path.join(self.raw_images_dir, class_name, img_filename)
                        cv2.imwrite(img_path, frame)
                        
                        # Save landmarks
                        landmark_filename = f"{class_name}_{start_index + samples_collected:04d}.npy"
                        landmark_path = os.path.join(self.landmarks_dir, class_name, landmark_filename)
                        np.save(landmark_path, landmarks)
                        
                        samples_collected += 1
                        last_capture_time = current_time
                        
                        # Visual feedback
                        cv2.rectangle(frame_with_hand, (0, 0), (w, h), (0, 255, 0), 15)
                        
                        if samples_collected % 50 == 0:
                            print(f"  ✓ {samples_collected + start_index}/{samples_to_collect + start_index} samples")
                    
                    # Ready indicator
                    cv2.circle(frame_with_hand, (w - 50, h - 50), 35, (0, 255, 0), -1)
                    cv2.putText(frame_with_hand, "OK", (w - 70, h - 40),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                else:
                    cv2.circle(frame_with_hand, (w - 50, h - 50), 35, (0, 0, 255), -1)
                    cv2.putText(frame_with_hand, "NO", (w - 70, h - 40),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
                # Instructions
                cv2.putText(frame_with_hand, "Move hand slightly | Press 'Q' to skip | 'P' to pause", 
                           (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                
                cv2.imshow('Custom Dataset Creator', frame_with_hand)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print(f"\n  Skipped with {samples_collected} samples")
                    break
                elif key == ord('p') or key == ord('P'):
                    print("\n  ⏸️  Paused - Press any key to continue...")
                    cv2.waitKey(0)
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        print(f"\n✅ Collected {samples_collected} new samples for '{class_name}'")
        print(f"   Total samples: {start_index + samples_collected}")
        
        return samples_collected
    
    def create_backup(self):
        """Create a timestamped backup of the dataset"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"dataset_backup_{timestamp}")
        
        print(f"\n💾 Creating backup...")
        shutil.copytree(self.base_dir, backup_path)
        print(f"✅ Backup created: {backup_path}")
        
        # Create a backup info file
        info_path = os.path.join(backup_path, "backup_info.txt")
        with open(info_path, 'w') as f:
            f.write(f"Backup created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Classes: {len(self.classes)}\n")
            f.write(f"Target samples per class: {self.samples_per_class}\n\n")
            
            for class_name in self.classes:
                img_count = len([f for f in os.listdir(os.path.join(backup_path, "raw_images", class_name)) 
                                if f.endswith('.jpg')])
                f.write(f"{class_name}: {img_count} samples\n")
        
        return backup_path
    
    def collect_full_dataset(self):
        """Collect data for all classes"""
        print("\n" + "="*70)
        print("  CUSTOM DATASET CREATOR")
        print("="*70)
        print(f"\nThis will collect YOUR personal ASL dataset:")
        print(f"  📊 Classes: {len(self.classes)} ({', '.join(self.classes[:10])}...)")
        print(f"  🎯 Samples per class: {self.samples_per_class}")
        print(f"  📈 Total samples: {len(self.classes) * self.samples_per_class}")
        print(f"  ⏱️  Estimated time: {len(self.classes) * 2} minutes")
        print(f"\n💾 Data will be saved to: {self.base_dir}")
        print(f"💾 Backups will be saved to: {self.backup_dir}")
        print("="*70)
        
        response = input("\nStart collection? (y/n): ").strip().lower()
        if response != 'y':
            return
        
        total_collected = 0
        
        for i, class_name in enumerate(self.classes, 1):
            print(f"\n\n{'='*70}")
            print(f"  PROGRESS: {i}/{len(self.classes)} classes")
            print(f"{'='*70}")
            
            collected = self.collect_class_data(class_name, self.samples_per_class)
            total_collected += collected
            
            # Create backup every 5 classes
            if i % 5 == 0:
                self.create_backup()
        
        # Final backup
        print(f"\n\n{'='*70}")
        print("  COLLECTION COMPLETE!")
        print(f"{'='*70}")
        print(f"\n📊 Statistics:")
        print(f"   Total samples collected: {total_collected}")
        print(f"   Classes: {len(self.classes)}")
        
        # Create final backup
        final_backup = self.create_backup()
        
        print(f"\n✅ Dataset creation complete!")
        print(f"   Dataset location: {self.base_dir}")
        print(f"   Final backup: {final_backup}")
        print(f"\n🚀 Next step: Train the model")
        print(f"   python train_custom_model.py")
        print("="*70)
    
    def show_statistics(self):
        """Show current dataset statistics"""
        print("\n" + "="*70)
        print("  DATASET STATISTICS")
        print("="*70)
        
        total_images = 0
        total_landmarks = 0
        
        print(f"\n{'Class':<10} {'Images':<10} {'Landmarks':<10}")
        print("-" * 30)
        
        for class_name in self.classes:
            img_count = len([f for f in os.listdir(os.path.join(self.raw_images_dir, class_name)) 
                            if f.endswith('.jpg')])
            landmark_count = len([f for f in os.listdir(os.path.join(self.landmarks_dir, class_name)) 
                                 if f.endswith('.npy')])
            
            total_images += img_count
            total_landmarks += landmark_count
            
            print(f"{class_name:<10} {img_count:<10} {landmark_count:<10}")
        
        print("-" * 30)
        print(f"{'TOTAL':<10} {total_images:<10} {total_landmarks:<10}")
        
        print(f"\n📊 Summary:")
        print(f"   Total samples: {total_landmarks}")
        print(f"   Average per class: {total_landmarks / len(self.classes):.1f}")
        print(f"   Completion: {(total_landmarks / (len(self.classes) * self.samples_per_class)) * 100:.1f}%")
        print("="*70)

def main():
    """Main menu"""
    creator = CustomDatasetCreator()
    
    while True:
        print("\n" + "="*70)
        print("  CUSTOM DATASET CREATOR - MAIN MENU")
        print("="*70)
        print("\n1. Collect Full Dataset (all classes)")
        print("2. Collect Specific Class")
        print("3. Show Statistics")
        print("4. Create Backup")
        print("5. Exit")
        print("="*70)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            creator.collect_full_dataset()
        elif choice == '2':
            print("\nAvailable classes:")
            for i, cls in enumerate(creator.classes, 1):
                print(f"  {i}. {cls}")
            
            cls_choice = input("\nEnter class name: ").strip().upper()
            if cls_choice in creator.classes:
                creator.collect_class_data(cls_choice, creator.samples_per_class)
            else:
                print("Invalid class name")
        elif choice == '3':
            creator.show_statistics()
        elif choice == '4':
            creator.create_backup()
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
