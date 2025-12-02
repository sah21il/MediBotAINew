"""
Supabase Cloud Storage Integration for Medical Records
"""
import os
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("Supabase not available, using local storage")

from dotenv import load_dotenv

load_dotenv()

class SupabaseStorage:
    def __init__(self):
        if not SUPABASE_AVAILABLE:
            raise ValueError("Supabase library not available")
            
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.bucket = os.getenv("SUPABASE_BUCKET", "medical-reports")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        
        self.client = create_client(url, key)
    
    def upload_file(self, file_content: bytes, file_path: str) -> str:
        """Upload file to Supabase Storage"""
        self.client.storage.from_(self.bucket).upload(file_path, file_content)
        return self.client.storage.from_(self.bucket).get_public_url(file_path)
    
    def download_file(self, file_path: str) -> bytes:
        """Download file from Supabase Storage"""
        return self.client.storage.from_(self.bucket).download(file_path)
    
    def delete_file(self, file_path: str):
        """Delete file from Supabase Storage"""
        self.client.storage.from_(self.bucket).remove([file_path])
    
    def list_files(self, folder: str = "") -> list:
        """List files in Supabase Storage"""
        return self.client.storage.from_(self.bucket).list(folder)
    
    def get_public_url(self, file_path: str) -> str:
        """Get public URL for file"""
        return self.client.storage.from_(self.bucket).get_public_url(file_path)

# Global instance
supabase_storage = None

def get_supabase_storage():
    global supabase_storage
    if supabase_storage is None:
        supabase_storage = SupabaseStorage()
    return supabase_storage
