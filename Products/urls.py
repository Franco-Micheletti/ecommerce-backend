from django.urls import path
from . import views

urlpatterns = [
    

    # Search With Filters
    path("products/product_name=<product_name>&filters=<filters>&page=<page>",views.SearchWithFilters.as_view()),
    # Search Without Filters
    path("products/product_name=<product_name>&page=<page>",views.SearchWithOutFilters.as_view()),
    # Products
    path("products/home",views.ProductsHome.as_view()),
    # Create Product
    path("product/create",views.Product.as_view()),
    # Get Product
    path("product/id=<id>",views.Product.as_view()),
    # Get Product By Property
    path("product/property=<property>&value=<value>",views.GetProductsByProperty.as_view()),
    # Get User's favorite products
    path("products/favorites/user_id=<id>",views.GetUserFavoriteProducts.as_view()),
    # Favorite Product ( Add - Delete )
    path("product/favorites/user_id=<user_id>&product_id=<product_id>",views.FavoriteProduct.as_view()),
    
    # REVIEWS 
    
    # Create user review
    path("product/review/product_id=<product_id>",views.UserReviewsEndpoint.as_view())
]