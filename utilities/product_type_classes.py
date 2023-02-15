from Products.models import CoffeTables,Laptops
from Products.serializers import CoffeTablesSerializer,LaptopsSerializer

product_types= {
            
                1:[CoffeTables,CoffeTablesSerializer],
                2:[Laptops,LaptopsSerializer]
            
            
               }