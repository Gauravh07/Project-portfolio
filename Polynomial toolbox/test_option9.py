import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: subtract\n\
###########################################\
")

p1=[2.0,-1.0,3.0]
p2=[1.0,1.0,2.0]
print("\nTest subtract function using p1=",p1,"and p2=",p2)
print("Correct answer: [1.0, -2.0, 1.0]")
print("Yours:",poly.subtract(p1,p2))


p1=[2.0,-1.0,3.0]
p2=[2.0,1.0]
print("\nTest subtract function using p1=",p1,"and p2=",p2)
print("Correct answer: [0.0, -2.0, 3.0]")
print("Yours:",poly.subtract(p1,p2))


print("\nTest subtract function using p1=",p2,"and p2=",p1)
print("Correct answer: [0.0, 2.0, -3.0]")
print("Yours:",poly.subtract(p2,p1))


p1=[3.0,1.0,2.0]
p2=[3.0,1.0,-2.0]
print("\nTest subtract function using p1=",p1,"and p2=",p2)
print("Correct answer: [0.0, 0.0, 4.0]")
print("Yours:",poly.subtract(p1,p2))



p1=[3.0,1.0,2.0]
p2=[3.0,1.0,2.0]
print("\nTest subtract function using p1=",p1,"and p2=",p2)
print("Correct answer: [0.0]")
print("Yours:",poly.subtract(p1,p2))

