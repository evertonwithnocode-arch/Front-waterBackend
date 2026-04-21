@router.post("/query")
def query(data: dict):
    return query_rag(
        question=data["question"],
        user_id=data["user_id"],
        entity=data.get("entity"),
        folder=data.get("folder")
    )