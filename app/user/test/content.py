from app.user.schema import UserCreate, UserRead


test_user_create = UserCreate(username='wumbo', email='foo@bar', password='password')
test_user = UserRead(username='wumbo', email='foo@bar', id=0, active=True)
