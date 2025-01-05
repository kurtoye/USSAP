import os
import pathlib

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print("GOOGLE_APPLICATION_CREDENTIALS:", credentials_path)

file_path = pathlib.Path(credentials_path.strip())
print("Path exists:", file_path.exists())
