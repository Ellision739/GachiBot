import asyncio
import pytest
from data_manager import db

@pytest.mark.asyncio
async def test_data_manager_flow():
    test_user_id = 999
    db.custom_usernames[test_user_id] = "Test Slave"

    await db.save_data("usernames")

    assert db.custom_usernames[test_user_id] == "Test Slave"
    print("✅ Тест пройден!")


if __name__ == "__main__":
    asyncio.run(test_data_manager_flow())