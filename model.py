#  import初始化flask-login的時候的login
from app_blog import login
#  接著加入callback function
@login.user_loader  
def load_user(user_id):  
    return UserRegister.query.get(int(user_id))