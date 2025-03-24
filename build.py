import PyInstaller.__main__
import os
import shutil

# Create dist directory if it doesn't exist
if not os.path.exists('dist'):
    os.makedirs('dist')

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Define paths
icon_path = 'assets/icon.png'  # Path to your PNG icon

# Run PyInstaller
PyInstaller.__main__.run([
    'main.py',  # Your main script
    '--name=GammaWatermarkRemover',
    '--onefile',  # Create a single executable
    '--windowed',  # Don't show console window
    '--add-data=config.py;.',  # Include config file
    '--add-data=watermark_detector.py;.',  # Include detector
    '--add-data=watermark_remover.py;.',  # Include remover
    f'--add-data={icon_path};assets',  # Include the icon file in the assets folder
    f'--icon={icon_path}',  # Use PNG format for the exe icon
    '--noconsole',  # No console window
    '--clean',  # Clean PyInstaller cache
])

# Copy additional required files to dist folder if needed
# For example:
# if os.path.exists('config.ini'):
#     shutil.copy('config.ini', 'dist/config.ini')

print("\nExecutable built successfully. Check the 'dist' folder.")
print(f"Icon used: {icon_path}")