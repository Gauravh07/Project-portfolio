import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: multiply\n\
###########################################\
")

p1=[1.0,2.0]
p2=[1.0,2.0]
print("\nTest multiply function using p1=",p1,"and p2=",p2)
print("Correct answer: [1.0, 4.0, 4.0]")
print("Yours:",poly.multiply(p1,p2))


p1=[1.0,2.0]
p2=[-1.0,2.0]
print("\nTest multiply function using p1=",p1,"and p2=",p2)
print("Correct answer: [-1.0, 0.0, 4.0]")
print("Yours:",poly.multiply(p1,p2))


p1=[4.0,-3.0,2.0,1.0,3.0]
p2=[-1.0,2.0,3.0,1.0]
print("\nTest multiply function using p1=",p1,"and p2=",p2)
print("Correct answer: [-4.0, 11.0, 4.0, -2.0, 2.0, 11.0, 10.0, 3.0]")
print("Yours:",poly.multiply(p1,p2))


p1=[5.0,-3.0,2.0]
p2=[0.0]
print("\nTest multiply function using p1=",p1,"and p2=",p2)
print("Correct answer: [0.0]")
print("Yours:",poly.multiply(p1,p2))
