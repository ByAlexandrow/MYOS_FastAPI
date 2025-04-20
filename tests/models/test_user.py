# import pytest
# from app.models.user import User
# from sqlalchemy import select

# # Тест для создания пользователя
# @pytest.mark.asyncio
# async def test_create_user(db_session):
#     new_user = User(
#         username='testuser',
#         email='testuser@example.com',
#         hashed_password='hashedpassword',
#         bio='This is a test user',
#         is_admin=False
#     )
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     assert new_user.id is not None
#     assert new_user.username == 'testuser'
#     assert new_user.email == 'testuser@example.com'
#     assert new_user.hashed_password == 'hashedpassword'
#     assert new_user.bio == 'This is a test user'
#     assert new_user.is_admin is False

# # Тест для чтения пользователя
# @pytest.mark.asyncio
# async def test_read_user(db_session):
#     new_user = User(
#         username='testuser',
#         email='testuser@example.com',
#         hashed_password='hashedpassword',
#         bio='This is a test user',
#         is_admin=False
#     )
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     result = await db_session.execute(select(User).filter_by(username='testuser'))
#     user = result.scalar_one_or_none()

#     assert user is not None
#     assert user.username == 'testuser'

# # Тест для обновления пользователя
# @pytest.mark.asyncio
# async def test_update_user(db_session):
#     new_user = User(
#         username='testuser',
#         email='testuser@example.com',
#         hashed_password='hashedpassword',
#         bio='This is a test user',
#         is_admin=False
#     )
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     new_user.bio = 'Updated bio'
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     assert new_user.bio == 'Updated bio'

# # Тест для удаления пользователя
# @pytest.mark.asyncio
# async def test_delete_user(db_session):
#     new_user = User(
#         username='testuser',
#         email='testuser@example.com',
#         hashed_password='hashedpassword',
#         bio='This is a test user',
#         is_admin=False
#     )
#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     await db_session.delete(new_user)
#     await db_session.commit()

#     result = await db_session.execute(select(User).filter_by(username='testuser'))
#     user = result.scalar_one_or_none()

#     assert user is None


