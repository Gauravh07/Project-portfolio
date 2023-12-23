import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: degree\n\
###########################################\
")

p=[4.5,5.0]
print("\nTest degree function using p=",p)
print("Correct answer: Degree is 1")
print("Yours:",poly.info(p))

p=[-2.0,0.0,2.0,0.0,3.0]
print("\nTest degree function using p=",p)
print("Correct answer: Degree is 4 and it is even")
print("Yours:",poly.info(p))

p=[0.0,1.0,0.0,-3.0,0.0]
print("\n(corner case) Test get_expression function using p=",p)
print("Correct answer: Degree is 3 and it is odd")
print("Yours:",poly.info(p))


p=[1.0]
print("\n(corner case) Test get_expression function using p=",p)
print("Correct answer: Degree is 0 and it is even")
print("Yours:",poly.info(p))
