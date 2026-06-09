async def get_user_documents(pool, user_id: int):
    async with pool.acquire() as conn:
        await conn.execute("SET app.user_id = $1", str(user_id))
        return await conn.fetch("SELECT * FROM documents")

async def create_document(pool, user_id: int, title: str, content: str):
    async with pool.acquire() as conn:
        await conn.execute("SET app.user_id = $1", str(user_id))
        return await conn.fetchrow(
            "INSERT INTO documents (user_id, title, content) VALUES ($1, $2, $3) RETURNING *",
            user_id, title, content
        )
