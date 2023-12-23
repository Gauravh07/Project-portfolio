###############################
# Team members- Please enter your names here
# Name1:Gaurav Hareesh 
# Name2:Anshuman Deodhar
###############################

# Modules
from Inventory import Inventory





'''------------------------------------------------------
                Main program starts here 
---------------------------------------------------------'''
# to complete

inventory=Inventory()
inventory.initialize()    
cart=Inventory()

print("welcome to BestMedia")
print("===============")
print('-------------------------------------------------------------------')
while True:
    print("1-List Inventory; 2-Info Inventory; 3-Search Inventory;4-Add Item; 5-Remove Item; 6-Inflation; 7-Shop; 8-Check-out" )

    command=input("Enter command:")
    if command=="":
        print("GoodBye!")
        break
    
    elif command=="1":
        print(inventory)

    elif command=='2':
        inventory.info()

    elif command=="3":
        Keyword=input("enter keyword to search for:")
        inventory.search(Keyword)

    elif command=='4':
        inventory.add()

    elif command=='5':
        inventory.delete()
    
    elif command=='6':
        x=int(input('Enter inflation %:'))
        inventory.adjust_price(x)

    elif command=='7':
        id=int(input("which item do you want to buy: "))    
        book=inventory.id_book(id)
        if book:
            cart.add(book)
            print('"%s" added to shopping cart!'%book.title)


    elif command=='8':
        
        if cart.books==[]:
            print('shopping cart is empty')
            break
        print('current shooping cart is: \n',cart)
        cart.info()
        promo_code=input('Enter your promotion code if any: ')
        if promo_code=='Voyage':
            cart.adjust_price(-5)
            print('updated shopping cart: \n',cart)
            cart.info()
        if promo_code=='Parfait':
            cart.adjust_price(-10) 
            print('updated shopping cart \n',cart)  
            cart.info()
        if promo_code=='':
            print('')
        
        creditcard=input("Enter your credit card number:")
        print('Purchase done!..Enjoy you new books')
        
        cart=Inventory()
                     


