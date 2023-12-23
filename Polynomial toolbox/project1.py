"""------------------------------------------------------
                 Import Modules 
---------------------------------------------------------"""
import polynomial as poly

"""------------------------------------------------------
                Main program starts here 
---------------------------------------------------------"""

print("\nPolynomial Tool")
print("===============")
# initialize the list of polynomials
list_poly=[]

# closed loop, keep executing until user press enter
while True:
    print("\n---------------")
    poly.display_list(list_poly) #display all current polynomials
    print("---------------")
    poly.display_menu()          #menu that contains all the options
    command=input("Enter Command: ")

    if command=="": #exit program      
        print("\nThanks for using the polynomial tool")
        print("Come back soon!")
        break
    
    elif command=="1": #insert a new polynomial in the list
        p=poly.get_polynomial() # transform entry (str) into list of floats
        list_poly=list_poly+[p]
        
    elif command=="2": #remove a polynomial from the list
        index=int(input("Which polynomial would you like to remove? "))
        if not(1<=index<=len(list_poly)):
            continue
        del(list_poly[index-1])
            
    elif command=="3": #display info (degrees) about polynomials
        for i in range(len(list_poly)):
            print(str(i+1)+': ',poly.info(list_poly[i]))
            
    elif command=="4": #evalute a given polynomial at different x values
        index=int(input("Which polynomial would you like to evaluate from [-3,3]? "))
        if not(1<=index<=len(list_poly)):
            continue
        for i in range(13):
            x=-3.0+i*0.5
            print(x,poly.evaluate(list_poly[index-1],x))
        
    elif command=="5": #scale all the coef of a given polynomial
        index=int(input("Which polynomial would you like to scale? "))
        if not(1<=index<=len(list_poly)):
            continue
        scale=float(input("Which scaling factor? "))
        p=poly.scale(list_poly[index-1],scale)
        print("%s*p%s(x)= %s"%(scale,index,poly.get_expression(p)))
        list_poly[index-1]=p # reinsert the scaled polynomial into the list
        
         
    elif command=="6": #display all the successive derivatives of a given polynomial
        index=int(input("Which polynomial would you like to derive? "))
        if not(1<=index<=len(list_poly)):
            continue
        dpdx=list_poly[index-1] # initialize polynomial to be derived
        d=len(dpdx)
        for i in range(d):
             dpdx=poly.derive(dpdx) # derive and store derivative
             print("("+str(i+1)+")",poly.get_expression(dpdx))
        
    elif command=="7": #evaluate the integral of a given polynomial between two bounds
        index=int(input("Which polynomial would you like to integrate? "))
        if not(1<=index<=len(list_poly)):
            continue
        lo=float(input("enter lower bound: "))
        up=float(input("enter upper bound: "))
        print("int(%s,%s) p%s(x) dx= %s"%(lo,up,index,poly.integrate(list_poly[index-1],lo,up)))
        
    elif command=="8": #add two polynomials and create a new one
        index1=int(input("Enter 1st polynomial #: "))
        index2=int(input("Enter 2nd polynomial #: "))
        if not(1<=index1<=len(list_poly)) or not(1<=index2<=len(list_poly)):
            continue
        p=poly.add(list_poly[index1-1],list_poly[index2-1])
        print("p%s(x)+p%s(x)= %s"%(index1,index2,poly.get_expression(p)))
        list_poly=list_poly+[p]
        
    elif command=="9": #subtract two polynomials and create a new one
        index1=int(input("Enter 1st polynomial #: "))
        index2=int(input("Enter 2nd polynomial #: "))
        if not(1<=index1<=len(list_poly)) or not(1<=index2<=len(list_poly)):
            continue
        p=poly.subtract(list_poly[index1-1],list_poly[index2-1])
        print("p%s(x)-p%s(x)= %s"%(index1,index2,poly.get_expression(p)))
        list_poly=list_poly+[p]
        
    elif command=="10": #multiply two polynomials and create a new one
        index1=int(input("Enter 1st polynomial #: "))
        index2=int(input("Enter 2nd polynomial #: "))
        if not(1<=index1<=len(list_poly)) or not(1<=index2<=len(list_poly)):
            continue
        p=poly.multiply(list_poly[index1-1],list_poly[index2-1])
        print("p%s(x)*p%s(x)= %s"%(index1,index2,poly.get_expression(p)))
        list_poly=list_poly+[p]
        
    elif command=="11":  #Bonus: divide two polynomials and display the factorization
        index1=int(input("Enter 1st polynomial #: "))
        index2=int(input("Enter 2nd polynomial #: "))
        if not(1<=index1<=len(list_poly)) or not(1<=index2<=len(list_poly)):
            continue
        poly.display_factorization(list_poly[index1-1],list_poly[index2-1])
