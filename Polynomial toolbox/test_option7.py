import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: integrate\n\
###########################################\
")

p=[1.0,0.0]
print("\nTest integrate function using p=",p,"between 0 and 2")
print("Correct answer: 2.0")
print("Yours:",poly.integrate(p,0,2))

p=[0.0,1.0]
print("\nTest integrate function using p=",p,"between 0 and 2")
print("Correct answer: 2.0")
print("Yours:",poly.integrate(p,0,2))



p=[0.0,0.0,1.0]
print("\nTest integrate function using p=",p,"between -3 and 3")
print("Correct answer: 18.0")
print("Yours:",poly.integrate(p,-3,3))


p=[0.0,1.0,0.0,1.0]
print("\nTest integrate function using p=",p,"between -2 and 2")
print("Correct answer: 0.0")
print("Yours:",poly.integrate(p,-2,2))
