from .user_routes import router as user_routes
from .auth_routes import router as auth_routes
all_routers = [
   user_routes,
   auth_routes
]