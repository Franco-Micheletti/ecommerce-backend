from Products.models import(
                            CoffeTables,
                            Laptops,
                            EnergyDrinks)
                    
from Products.serializers import(
                                CoffeTablesSerializer,
                                LaptopsSerializer,
                                EnergyDrinksSerializer)

product_types= {
            
                1:[CoffeTables,CoffeTablesSerializer],
                2:[Laptops,LaptopsSerializer],
                5:[EnergyDrinks,EnergyDrinksSerializer]
               }