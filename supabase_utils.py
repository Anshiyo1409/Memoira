import time
from supabase import create_client, Client

SUPABASE_URL = "https://mmtihotoyetxcoinbvcw.supabase.co"
SUPABASE_KEY = "sb_secret_HvrTQ3PL5nkCMqK8gRIOeQ_o1XdEOMq" # Your Key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(file, folder="memories"):
    """
    Uploads a file to Supabase Storage with unique naming to avoid RLS 403 errors.
    """
    # 1. Create a unique filename using timestamp to avoid "New row violates RLS" 
    # which often happens when trying to overwrite an existing file.
    file_name = getattr(file, "name", "upload.png")
    timestamp = int(time.time())
    unique_name = f"{timestamp}_{file_name}"
    path = f"{unique_name}" # Path inside the bucket

    file_bytes = file.read() if hasattr(file, "read") else file
    
    try:
        # 2. Perform the upload
        # We use 'x-upsert': 'true' so that if the file exists, it overwrites 
        # (Note: Overwriting requires an UPDATE RLS policy)
        response = supabase.storage.from_("memories").upload(
            path=path,
            file=file_bytes,
            file_options={"content-type": "image/png", "x-upsert": "true"}
        )
        
        # 3. Get the public URL
        url_data = supabase.storage.from_("memories").get_public_url(path)
        return url_data
        
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

def save_memory_to_db(memory_text, audio_url=None, image_url=None, doc_url=None):
    """Save memory metadata to Supabase DB."""
    return supabase.table("memories").insert({
        "memory_text": memory_text,
        "audio_path": audio_url,
        "image_path": image_url,
        "doc_path": doc_url
    }).execute()

def fetch_memories():
    """Fetch all memories."""
    response = supabase.table("memories").select("*").order("created_at", desc=True).execute()
    return response.data