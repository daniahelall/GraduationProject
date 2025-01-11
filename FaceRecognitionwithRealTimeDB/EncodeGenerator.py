import cv2
import face_recognition
import pickle
import os
from supabase import create_client, Client

# Initialize Supabase
SUPABASE_URL = "https://nugmsadjxlyswwkstglm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51Z21zYWRqeGx5c3d3a3N0Z2xtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMjc5ODQzMywiZXhwIjoyMDQ4Mzc0NDMzfQ.kiKSm_sMOnoUqJXRMhYzHVPGvfkjU56F4ws2SO7g60g"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Supabase initialized!")

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

bucket_name = "images"

for path in pathList:
    filePath = path

    try:
        # Attempt to fetch file metadata to check if it exists
        file_metadata = supabase.storage.from_(bucket_name).get_metadata(filePath)
        if file_metadata:
            print(f"File {filePath} already exists in Supabase. Skipping upload.")
            continue
    except Exception:
        # File does not exist in storage, proceed to upload
        pass

    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    # Upload image to Supabase storage bucket
    filePath = os.path.join(folderPath, path)
    with open(filePath, "rb") as file:
        file_data = file.read()

    try:
        # Upload the file to Supabase storage
        response = supabase.storage.from_(bucket_name).upload(path, file_data)
        if response.status_code == 200:
            print(f"Successfully uploaded {filePath} to Supabase storage.")
        else:
            print(f"Failed to upload {filePath}. Response: {response.error_message}")
    except Exception as e:
        print(f"Failed to upload {filePath}: {e}")

# Function to encode images
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encodeList.append(encode[0])  # Assuming one face per image
    return encodeList

# Encode the images
print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encodings to a pickle file
file_name = "EncodeFile.p"
with open(file_name, 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("Encoding file saved.")

# Upload the pickle file to Supabase
with open(file_name, "rb") as file:
    pickle_data = file.read()

try:
    # Upload the pickle file to Supabase
    response = supabase.storage.from_(bucket_name).upload(file_name, pickle_data)
    if response.status_code == 200:
        print(f"Successfully uploaded {file_name} to Supabase storage.")
    else:
        print(f"Failed to upload {file_name}. Response: {response.error_message}")
except Exception as e:
    print(f"Failed to upload {file_name}: {e}")
