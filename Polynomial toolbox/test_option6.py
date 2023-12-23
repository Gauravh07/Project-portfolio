import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: derive\n\
###########################################\
")

p=[3.0,2.0]
print("\nTest derive function using p=",p)
print("Correct answer: [2.0]")
print("Yours:",poly.derive(p))


p=[7.5,5.0,3.0,-2.0]
print("\nTest derive function using p=",p)
print("Correct answer: [5.0, 6.0, -6.0]")
print("Yours:",poly.derive(p))


p=[-2.0]
print("\nTest derive function using p=",p)
print("Correct answer: [0.0]")
print("Yours:",poly.derive(p))

