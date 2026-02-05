from .user_routes import router as user_routes
from .auth_routes import router as auth_routes
from .category_routes import router as category_routes
from .product_routes import router as product_routes

all_routers = [
   user_routes,
   category_routes,
   product_routes,
   auth_routes
]