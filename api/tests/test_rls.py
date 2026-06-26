import pytest
import asyncpg

async def get_admin_conn():
    return await asyncpg.connect(
        "postgresql://postgres:postgres@localhost/datagate"
    )

async def get_app_conn():
    return await asyncpg.connect(
        "postgresql://app_user:changeme@localhost/datagate"
    )

@pytest.mark.asyncio
async def test_rls_isolation():
    admin = await get_admin_conn()
    app = await get_app_conn()

    # cleanup
    await admin.execute("DELETE FROM documents")
    await admin.execute("DELETE FROM users WHERE email IN ('user_a@test.com', 'user_b@test.com')")

    # create two users
    user_a = await admin.fetchrow(
        "INSERT INTO users (email) VALUES ($1) RETURNING id",
        "user_a@test.com"
    )
    user_b = await admin.fetchrow(
        "INSERT INTO users (email) VALUES ($1) RETURNING id",
        "user_b@test.com"
    )

    # insert doc as user_a
    await app.execute(f"SET app.user_id = '{user_a['id']}'")
    await app.execute(
        "INSERT INTO documents (user_id, title) VALUES ($1, $2)",
        user_a["id"], "secret doc"
    )

    # read as user_b
    await app.execute(f"SET app.user_id = '{user_b['id']}'")
    docs = await app.fetch("SELECT * FROM documents")

    assert len(docs) == 0

    await admin.close()
    await app.close()
