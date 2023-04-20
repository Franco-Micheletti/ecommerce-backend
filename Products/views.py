from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
from .models import ProductsModel,Properties,Values,PropertyValuePairs,ProductProperties,Brand,ProductVariants,Favorites,UserReviews
from ProductTypes.models import ProductTypes
from .serializers import (ProductsSerializer,PropertiesSerializer,ValuesSerializer,PropertyValuePairsSerializer,
ProductPropertiesSerializer,GetProductByPropertySerializer,FavoritesSerializer,UserReviewsSerializer,UserReviewsProductOnlySerializer)
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR)
from django.db.models import Q
from django.db.models import Count,Max,Avg
import math
from Products.functions.product_has_property_value_pair import product_has_property_value_pair
from Products.functions.count_property_values_results import count_property_values_results
from Products.functions.filter_products import filter_products
from login.models import CustomUser
import jwt
from datetime import date as date

class SearchWithFilters(APIView):
    """
    METHODS:

    GET

    Returns products and filters filtering by product name and user applied filters
    """
    def get(self,request,filters,product_name,page=1,order_by_string=None):
        
        if product_name and filters and page:
            
            products = ProductsModel.objects.filter(product_name__icontains=str(product_name))
            
            # Check if any sort by was selected
            if order_by_string:
                # Replace speed by shipping days
                if "speed" in order_by_string:
                    order_by_string.replace("speed","shipping_days")
                order_by_list = order_by_string.split("+")
                products = products.order_by(*order_by_list)[0:1000]

            if products:
                # Create dictionary with the sum of each property value.
                response_data = count_property_values_results(product_name)
                # Apply filters selected by the user before serializing
                products_list = filter_products(filters,products)
                # Pagination
                total_products    = products
                filtered_products = products_list[(int(page)-1)*30:int(page)*30]
                # Serializing products
                products_data = ProductsSerializer(filtered_products,many=True).data
                # Get the maximum price of all products
                max_price = products.aggregate(Max('price'))
                response_data["filters"]["price"]["max_price"] = max_price['price__max']
                # Add products to response data
                response_data["products"] = products_data
                # Create list of pages to render pages button in frontend
                response_data["pages"] = [ x for x in range(1,math.ceil((len(total_products))/30)+1)]
                response_data["total_results"] = len(total_products)
                
                return Response(response_data,status=HTTP_200_OK)
            else:
                return Response({"match":0},status=HTTP_200_OK)
        else:
            response_data = {"message":"Missing parameters"}
            return Response(response_data,status=HTTP_400_BAD_REQUEST)

class SearchWithOutFilters(APIView):
    """
    METHODS:
    
    GET

    Returns products and filters filtering by product name
    """
    def get(self,request,product_name,page,order_by_string=None):
        
        if product_name:
                
                response_data = {
                    "filters":{
                        "price":{
                            "max_price":0
                        }
                    }
                }

                # Search by product name
                products = ProductsModel.objects.filter(product_name__icontains=str(product_name))
                # Check if any sort by was selected
                if order_by_string:
                    # Replace speed by shipping days
                    if "speed" in order_by_string:
                        order_by_string = order_by_string.replace("speed","shipping_days")
                    
                    order_by_list = order_by_string.split(",")
                    
                    products = products.order_by(*order_by_list)[0:1000]
                
                product_properties = ProductProperties.objects.filter(product__product_name__icontains=str(product_name))[0:1000]
                if product_properties:
                    for object in product_properties:
                        name = object.property_value_pair.property.property_name
                        value = object.property_value_pair.value.value_name
                        try:
                            response_data["filters"][name][value] += 1
                        except:
                            if name in response_data["filters"]:
                                response_data["filters"][name][value] = 1
                            else:
                                response_data["filters"][name] = {}
                                response_data["filters"][name][value] = 1

                if product_properties:
                    
                    # Results per page

                    products_slice = products[(int(page)-1)*30:int(page)*30]
                    
                    # Serializing objects

                    products_data = ProductsSerializer(products_slice,many=True).data

                    # Add products to response data

                    response_data["products"] = products_data

                    # Get the maximum price of all products

                    max_price = products.aggregate(Max('price'))
                    response_data["filters"]["price"]["max_price"] = max_price['price__max']

                    # Add list of pages to render pages button in frontend

                    response_data["pages"] = [ x for x in range(1,math.ceil((len(products))/30)+1)]
                    response_data["total_results"] = len(products)
                    
                    return Response(response_data,status=HTTP_200_OK)
                else:
                    return Response({"match":0},status=HTTP_200_OK) 
        else:
            response_data = {"message":"Product name not provided"}
            return Response(response_data,status=HTTP_400_BAD_REQUEST)
        
class Product(APIView):

    def post(self,request):

        request_data = request.data
        
        # Create product basic info
        new_product = ProductsModel.objects.create(
            
            product_name         = request_data["product_name"],
            product_image_tag    = request_data["product_image_tag"],
            generic_image_tag    = request_data["generic_image_tag"],
            total_images         = request_data["total_images"],
            product_type         = ProductTypes.objects.get(id=request_data["product_type_id"]),
            brand                = Brand.objects.get(id=request_data["brand_id"]),
            price                = request_data["price"],
            retailer             = request_data["retailer"],
            availability         = request_data["availability"],
            shipping_days        = request_data["shipping_days"],
            pack                 = request_data["pack"]
        )

        # Check if product have variants

        if request_data["variant_options"] and request_data["variant_id"]:
            
            new_product.variant_id = request_data["variant_id"]
            new_product.variant_options = request_data["variant_options"]

            new_product.save()

            ProductVariants.objects.create(
                product    = new_product,
                variant_id = request_data["variant_id"],
                values     = request_data["variant_values"]
            )
            
        # Create properties
        properties = request_data["properties"]
        if properties:
            for dict_ in properties:
                
                property = Properties.objects.get_or_create(property_name=dict_[0])
                value    = Values.objects.get_or_create(value_name=dict_[1])
                property_value_pair = PropertyValuePairs.objects.get_or_create(property=property[0],value=value[0])
                product_properties  = ProductProperties.objects.get_or_create(product=new_product,property_value_pair=property_value_pair[0])

            response_data = {
                "message":"product created successfully",
                "product":new_product.id
            }
        
            return Response(response_data,status=HTTP_200_OK)
        else:
            return Response("Properties are required",HTTP_400_BAD_REQUEST)
         
    def get(self,request,id):

        try:
            product = ProductsModel.objects.get(id=id)
        except ProductsModel.DoesNotExist:
            return Response("No product have been found with the ID provided")
        
        response_data = {}
        

        try:
            access_token = request.COOKIES.get("jwt_access")
            if access_token:
                try:
                    user_data = jwt.decode(jwt=access_token,
                                           key=settings.SECRET_KEY,
                                           verify=True,
                                           algorithms=["HS256"])
                    
                    # Get the review of the logged user

                    logged_user = CustomUser.objects.get(id=user_data["user_id"])
                    logged_user_review = UserReviews.objects.get(product=product,user=logged_user)

                    if logged_user_review:
                        logged_user_review_data = UserReviewsSerializer(logged_user_review).data
                        response_data["logged_user_review"] = logged_user_review_data
                        
                except Exception as e:
                    print(e)
                    
        except Exception as e:
            print(e)
        
        # Get all product's reviews
        try:
            
            all_reviews          = UserReviews.objects.filter(product=product)
            reviews_without_user = all_reviews.exclude(user=user_data["user_id"])
        except:
            all_reviews = UserReviews.objects.filter(product=product)
            
        if all_reviews:
            try:
                reviews_data = UserReviewsSerializer(reviews_without_user,many=True).data
            except:
                reviews_data = UserReviewsSerializer(all_reviews,many=True).data
            
            response_data["reviews"] = reviews_data

            # Get average score of the product
            average_score = all_reviews.aggregate(Avg('score'))

            response_data["avg_score"] = {}
            response_data["avg_score"]["avg"]           = average_score["score__avg"]
            response_data["avg_score"]["total_reviews"] = len(all_reviews)

        # Get product properties

        product_properties_queryset = ProductProperties.objects.filter(product=product)
        properties_data = {object.property_value_pair.property.property_name:object.property_value_pair.value.value_name for object in product_properties_queryset }
        
        response_data["basic"] = ProductsSerializer(product).data
        response_data["properties"] = properties_data
    
        # Check if product have variants

        if product.variant_id and product.variant_options:
            variants_objects = ProductVariants.objects.filter(variant_id=product.variant_id)
            variants_data = []
            for object in variants_objects:
                variants_data.append(
                    {"id"    :(object.product.id),
                    "values":object.values })
            
            response_data["variant_data"]    = variants_data
            response_data["variant_options"] = dict(sorted(product.variant_options.items(),reverse=True))

        return Response(response_data,status=HTTP_200_OK)
        
    def delete(self,request,id):

        product = ProductsModel.objects.get(id=id)

        if product:
            product.delete()

            return Response("Product deleted successfully",HTTP_200_OK)
        else:
            return Response("Product doesn't exist",HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):

        return Response({},HTTP_200_OK)
    
class ProductsHome(APIView):

    def get(self,request):

        def calculate_avg_score(products_data): 
            
            for product in products_data:

                product_reviews = UserReviews.objects.filter(product_id=product["id"])
                # Get average score of the product
                average_score = product_reviews.aggregate(Avg('score'))
                product["avg_score"] =  {
                                            "avg":average_score,
                                            "total_reviews": len(product_reviews)
                                        }
            return products_data
            
        cookies       = ProductsModel.objects.filter(product_type_id=4)
        cookies_data  = ProductsSerializer(cookies,many=True).data
        cookies_data  = calculate_avg_score(cookies_data)
        
        laptops       = ProductsModel.objects.filter(product_type_id=2)
        laptops_data  = ProductsSerializer(laptops,many=True).data
        laptops_data  = calculate_avg_score(laptops_data)

        energy_drinks       = ProductsModel.objects.filter(product_type_id=5)
        energy_drinks_data  = ProductsSerializer(energy_drinks,many=True).data
        energy_drinks_data  = calculate_avg_score(energy_drinks_data)
        
        response_data = {
                            "cookies":      cookies_data,
                            "laptops":      laptops_data,
                            "energy_drinks":energy_drinks_data
                         }
        
        return Response(response_data,status=HTTP_200_OK)
        
class GetProductsByProductType(APIView):

    def get(self,request,product_type_id):
        
        products      = ProductsModel.objects.get(product_type_id=product_type_id)
        products_data = ProductsSerializer(products,many=True).data
        
        if products:
            return Response(products_data,status=HTTP_200_OK)
        else:
            return Response({},HTTP_200_OK)
   
class GetProductsByProperty(APIView):

    def get(self,request,property,value):

        response_data = {}
        
        try:
            property_object = Properties.objects.get(property_name=property)
            value_object    = Values.objects.get(value_name=value)
            property_value_pair = PropertyValuePairs.objects.get(property=property_object,value=value_object)
        except:
            return Response("Property/Value pair not found",status=HTTP_400_BAD_REQUEST)
        product_properties_objects = ProductProperties.objects.filter(property_value_pair=property_value_pair)
        
        if product_properties_objects:
            
            for index,object in enumerate(product_properties_objects):
                product_properties_queryset = ProductProperties.objects.filter(product=object.product)
                properties_data = {object.property_value_pair.property.property_name:object.property_value_pair.value.value_name for object in product_properties_queryset }
                response_data[index] = ProductsSerializer(object.product).data
                response_data[index]["properties"] = properties_data        

            return Response(response_data,status=HTTP_200_OK)                                  
        
        else:
            return Response("Property pair not found",status=HTTP_400_BAD_REQUEST)
        
class GetUserFavoriteProducts(APIView):

    def get(self,request,id):
        
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"message":"User does not exist"},status=HTTP_400_BAD_REQUEST)
        
        try:
            favorites = Favorites.objects.filter(user=user)
        except Favorites.DoesNotExist:
            return Response({"message":"User doesn't have any favorites yet"},status=HTTP_400_BAD_REQUEST)


        favorite_products_list = [ favorite_object.product for favorite_object in favorites ]
        favorite_products_data = ProductsSerializer(favorite_products_list,many=True).data
        favorite_icon_change_list = [ product.id for product in favorite_products_list ]


        response_data = {"favorite_products_data":favorite_products_data,
                         "icon_change_list":favorite_icon_change_list}

        return Response(response_data,status=HTTP_200_OK)

class FavoriteProduct(APIView):

    # Add favorite product
    def post(self,request,product_id,user_id):
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"message":"User does not exist"},status=HTTP_400_BAD_REQUEST)
        
        try:
            product = ProductsModel.objects.get(id=product_id)
        except ProductsModel.DoesNotExist:
            return Response({"message":"Product does not exist"},status=HTTP_400_BAD_REQUEST)
        
        try:
            Favorites.objects.create(

                user = user,
                product = product
            )
        except:
            return Response({"message":"Error creating favorite"},status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Response with updated list

        try:
            favorites = Favorites.objects.filter(user=user)
        except Favorites.DoesNotExist:
            return Response({"message":"User doesn't have any favorites yet"},status=HTTP_400_BAD_REQUEST)
    
        favorite_products_list = [ favorite_object.product for favorite_object in favorites ]
        favorite_products_data = ProductsSerializer(favorite_products_list,many=True).data
        favorite_icon_change_list = [ product.id for product in favorite_products_list ]


        response_data = {"message":"Product added to favorites successfully",
                         "favorite_products_data":favorite_products_data,
                         "icon_change_list":favorite_icon_change_list}
        
        return Response(response_data,status=HTTP_200_OK) 
        
    def delete(self,request,product_id,user_id):
        
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"message":"User does not exist"},status=HTTP_400_BAD_REQUEST)

        try:
            product = ProductsModel.objects.get(id=product_id)
        except ProductsModel.DoesNotExist:
            return Response({"message":"Product does not exist"},status=HTTP_400_BAD_REQUEST)
        
        try:
            favorite_product = Favorites.objects.get(user=user,product=product)
        except Favorites.DoesNotExist:
            return Response({"message":"User doesn't have any favorites yet"},status=HTTP_400_BAD_REQUEST)

        try:
            favorite_product.delete()
        except:
            return Response({"message":"Error creating favorite"},status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Response with updated list

        try:
            favorites = Favorites.objects.filter(user=user)
        except Favorites.DoesNotExist:
            return Response({"message":"User doesn't have any favorites yet"},status=HTTP_400_BAD_REQUEST)
    
        favorite_products_list = [ favorite_object.product for favorite_object in favorites ]
        favorite_products_data = ProductsSerializer(favorite_products_list,many=True).data
        favorite_icon_change_list = [ product.id for product in favorite_products_list ]


        response_data = {"message":"Product removed from favorites successfully",
                        "favorite_products_data":favorite_products_data,
                        "icon_change_list":favorite_icon_change_list}
        
        return Response(response_data,status=HTTP_200_OK) 
        
class UserReviewsEndpoint(APIView):

    def put(self,request,review_id):

        request_data = request.data

        access_token = request.COOKIES.get("jwt_access")

        if access_token:
            user_data = jwt.decode(jwt=access_token,
                                   key=settings.SECRET_KEY,
                                   verify=True,
                                   algorithms=["HS256"]) 
            
            user      = CustomUser.objects.get(id = user_data["user_id"])
            review    =  UserReviews.objects.get(id=review_id)
            
            if user:
                if review:
                    # Check if user is the same user that created the review
                    if user == review.user:
                        
                        # Update text
                        if len(request_data["text"]) >= 20:
                            review.text = request_data["text"]
                        else:
                            return Response({"error":"The review should be at least 20 characters long"},HTTP_400_BAD_REQUEST)
                        
                        # Update score
                        if request_data["score"] != "":
                            review.score = request_data["score"]
                        else:
                            return Response({"error":"Score is required"},HTTP_400_BAD_REQUEST)    
                        
                        review.date = date.today()
                        
                        review.save()
                        
                    new_review_data = UserReviewsSerializer(review).data

                    return Response(new_review_data,HTTP_200_OK)
                else:
                    return Response("Review not found",HTTP_400_BAD_REQUEST)
            else:
                return Response("User is not valid",HTTP_401_UNAUTHORIZED)
        else:
            return Response("Not authorization provided",HTTP_401_UNAUTHORIZED)

    def post(self,request,product_id):

        request_data = request.data

        access_token = request.COOKIES.get("jwt_access")

        if access_token:
            user_data = jwt.decode(jwt=access_token,
                                   key=settings.SECRET_KEY,
                                   verify=True,
                                   algorithms=["HS256"]) 
            
            product   = ProductsModel.objects.get(id = product_id)
            user      = CustomUser.objects.get(id = user_data["user_id"])
            
            if user:
                if product:

                    new_review = UserReviews.objects.create(

                        text    = request_data["text"],
                        score   = request_data["score"],
                        product = product,
                        user    = user,
                        date    = date.today()
                    )

                    new_review_data = UserReviewsSerializer(new_review).data

                    return Response(new_review_data,HTTP_200_OK)
                else:
                    return Response("Product removed or id not valid",HTTP_400_BAD_REQUEST)
            else:
                return Response("User is not valid",HTTP_401_UNAUTHORIZED)
        else:
            return Response("Not authorization provided",HTTP_401_UNAUTHORIZED)

    def delete(self,request,review_id):

        access_token = request.COOKIES.get("jwt_access")

        if access_token:
            user_data = jwt.decode(jwt=access_token,
                                   key=settings.SECRET_KEY,
                                   verify=True,
                                   algorithms=["HS256"]) 
            
            user      = CustomUser.objects.get(id = user_data["user_id"])
            review    = UserReviews.objects.get(id=review_id)
            
            if user:
                if review:
                    review.delete()

                    return Response("Review deleted successfully",HTTP_200_OK)
                else:
                    return Response("Review not found",HTTP_400_BAD_REQUEST)
            else:
                return Response("User is not valid",HTTP_401_UNAUTHORIZED)
        else:
            return Response("Not authorization provided",HTTP_401_UNAUTHORIZED)
        
class GetAllReviewsOfUser(APIView):

    def get(self,request):
        
        if "jwt_access" in request.COOKIES:
            access_token = request.COOKIES.get("jwt_access")

            if access_token:
                
                user_data = jwt.decode(jwt=access_token,
                                    key=settings.SECRET_KEY,
                                    verify=True,
                                    algorithms=["HS256"]) 
                try:
                    user = CustomUser.objects.get(id = user_data["user_id"])
                except CustomUser.DoesNotExist:
                    return Response("Not authorized",HTTP_401_UNAUTHORIZED)
                
                reviews_of_user = UserReviews.objects.filter(user=user)
                if reviews_of_user:
                    reviews_of_user_data = UserReviewsSerializer(reviews_of_user,many=True).data
                    return Response(reviews_of_user_data,HTTP_200_OK)
                else:
                    return Response({},HTTP_200_OK)
                
            else:
                return Response("No token provided or invalid",HTTP_404_NOT_FOUND)
        else:
            return Response("Credentials were not provided")

class GetMostPopularProducts(APIView):

    def get(self,request):
        
        popular_review_items  = UserReviews.objects.filter(score__gt=3.8).order_by('-product__price')[:1000]
        popular_products_list = []
        product_ids_list = []
        for item in popular_review_items:
            if item.product.id not in product_ids_list:
                popular_products_list.append(item.product)
                product_ids_list.append(item.product.id)
            else:
                continue
            
        most_popular_products_data = ProductsSerializer(popular_products_list[0:12],many=True).data

        if popular_review_items:
            return Response(most_popular_products_data,HTTP_200_OK)
        else:
            return Response({},HTTP_200_OK)
        
