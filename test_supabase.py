# test_supabase.py
from supabase import create_client, Client

SUPABASE_URL = "https://mmtihotoyetxcoinbvcw.supabase.co"  # replace with your Supabase URL
SUPABASE_KEY = "sb_secret_HvrTQ3PL5nkCMqK8gRIOeQ_o1XdEOMq"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert a test memory
response = supabase.table("memories").insert({
    "memory_text": "This is a test memory",
    "audio_path": None,
    "image_path": None,
    "doc_path": None
}).execute()

print(response)