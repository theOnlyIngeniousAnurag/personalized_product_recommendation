import os
import shutil
import kagglehub

print("Starting RetailRocket download via kagglehub...")
downloaded_path = kagglehub.dataset_download("retailrocket/ecommerce-dataset")
print(f"Downloaded path: {downloaded_path}")

target_dir = "/app/applet/data/raw/retailrocket"
os.makedirs(target_dir, exist_ok=True)

files = os.listdir(downloaded_path)
print(f"Found files: {files}")

for filename in files:
    src = os.path.join(downloaded_path, filename)
    dst = os.path.join(target_dir, filename)
    if os.path.isfile(src):
        print(f"Copying {filename} ({os.path.getsize(src)} bytes) to {dst}...")
        shutil.copy2(src, dst)
        print(f"Copied {filename} successfully.")

print("All RetailRocket raw files successfully copied to:", target_dir)
print("Listing target directory:")
for f in os.listdir(target_dir):
    p = os.path.join(target_dir, f)
    print(f" - {f}: {os.path.getsize(p)} bytes")
