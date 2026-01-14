import subprocess
import sys
from datetime import datetime

def run_command(cmd, description):
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ {description} failed!")
        return False
    return True

def main():
    print("\n" + "="*60)
    print("  COMPLETE PIPELINE: Firebase → Excel → Train → Predict")
    print("="*60)
    
    steps = [
        ("python fetch_firebase.py", "STEP 1: Fetch data from Firebase"),
        ("python train_model.py", "STEP 2: Train ML Model"),
        ("python predict.py", "STEP 3: Make Predictions"),
    ]
    
    for i, (cmd, desc) in enumerate(steps, 1):
        success = run_command(cmd, desc)
        if not success:
            print(f"\n⚠️  Pipeline stopped at step {i}")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("  ✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Check data.xlsx, data.csv for updated data\n")

if __name__ == "__main__":
    main()
