import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: get_expression\n\
###########################################"\
      )

p1=[4.5,5.0]   
print("\nTest get_expression function using p1=",p1)
print("Acceptable answer or similar (easier): (4.5)x^0+(5.0)x^1")
print("Correct answer (for full credit): 4.5+5.0x")
print("Yours:",poly.get_expression(p1))

p2=[-4.5,-5.0]   
print("\nTest get_expression function using p2=",p2)
print("Acceptable answer or similar (easier): (-4.5)x^0+(-5.0)x^1")
print("Correct answer (for full credit): -4.5-5.0x")
print("Yours:",poly.get_expression(p2))


p3=[2.0,0.0,3.0]
print("\nTest get_expression function using p3=",p3)
print("Acceptable answer or similar (easier): (2.0)x^0+(0.0)x^1+(3.0)x^2")
print("Correct answer (for full credit): 2.0+3.0x^2")
print("Yours:",poly.get_expression(p3))

p4=[0.0,0.0,0.0]
print("\nTest get_expression function using p4=",p4)
print("Acceptable answer or similar (easier): (0.0)x^0+(0.0)x^1+(0.0)x^2")
print("Correct answer (for full credit): 0.0")
print("Yours:",poly.get_expression(p4))

p5=[]
print("\nTest get_expression function using p5=",p5)
print("Correct answer (for full credit): 0.0")
print("Yours:",poly.get_expression(p5))


print("\n\
###########################################\n\
#### Test for the function: display_list\n\
#### (it must call the function get_expression)\n\
###########################################\
")

list_poly=[p1,p2,p3,p4]
print("\nTest display_list function for polynomials p1-p2-p3-p4")
print("Correct answer (depends on your get_expression output answers):")
print("1: 4.5+5.0x","2: -4.5-5.0x","3: 2.0+3.0x^2","4: 0.0",sep="\n")
print("Yours:")
poly.display_list(list_poly)
