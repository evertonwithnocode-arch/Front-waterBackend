from app.db.supabase_client import supabase

def get_user_role(user_id: str):
    response = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    
    if not response.data:
        raise Exception("User not found")
    
    return response.data[0]["role"]