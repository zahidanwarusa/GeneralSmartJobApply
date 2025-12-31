import os
from supabase import create_client, Client
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY')

def get_supabase_client() -> Client:
    """
    Get Supabase client instance
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")

    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Global client instance
supabase: Client = None

def init_supabase():
    """
    Initialize Supabase client
    """
    global supabase
    if supabase is None:
        supabase = get_supabase_client()
    return supabase
