from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_role(user_id):
    res = supabase.table("profiles") \
        .select("role") \
        .eq("user_id", user_id) \
        .execute()

    if not res.data:
        raise Exception("User not found in profiles")

    return res.data[0]["role"]