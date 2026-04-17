from app.core.chroma_client import get_chroma
from app.services.supabase_service import get_user_role

def get_allowed_collections(workflow):

    if workflow == "XPC_customer_eval":
        return ["xpc_internal", "xpc_validations", "shared_science"]

    if workflow == "Frontwater_review":
        return ["frontwater_internal", "sio_data"]

    return []