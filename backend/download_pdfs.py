import os
import requests

downloads = {
    "cassava_cropping.pdf": "https://www.iita.org/wp-content/uploads/2016/06/Cassava_system_cropping_guide.pdf",
    "rice_northern_nigeria.pdf": "https://www.iita.org/wp-content/uploads/2020/07/Guide-to-Rice-Production-in-Northern-Nigeria.pdf",
    "rice_training_manual.pdf": "https://agrinigeriaprodsa.blob.core.windows.net/agrifarmer/9f50c4ab-2074-4bae-97f3-50ef085ba9cb.pdf",
    "maize_training_manual.pdf": "https://agrinigeriaprodsa.blob.core.windows.net/agrifarmer/ac6c4faf-04c0-42a1-9fe0-e7a9b5e7d652.pdf",
    "maize_northern_nigeria.pdf": "https://www.iita.org/wp-content/uploads/2020/07/Guide-to-Maize-Production-in-Northern-Nigeria.pdf",
    "cowpea_manual.pdf": "https://www.iita.org/wp-content/uploads/2020/05/Cowpea-manualENGLISH.pdf",
    "yam_seed_production.pdf": "https://biblio.iita.org/documents/U17ManMaroyaManualNothomNodev.pdf-df18c171d9ed4a6e4de21c0e9926cfe2.pdf"
}

output_dir = r"c:\Users\Excellus\Documents\AgriSabi\docs\raw_data"
os.makedirs(output_dir, exist_ok=True)

for filename, url in downloads.items():
    filepath = os.path.join(output_dir, filename)
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Success: {filename}")
        else:
            print(f"Failed to download {filename}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
