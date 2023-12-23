import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: add\n\
###########################################\
")

p1=[-1.0,3.0]
p2=[-1.0,3.0]
print("\nTest add function using p1=",p1,"and p2=",p2)
print("Correct answer: [-2.0, 6.0]")
print("Yours:",poly.add(p1,p2))


p1=[2.0,-1.0,3.0]
p2=[3.0,1.0,2.0]
print("\nTest add function using p1=",p1,"and p2=",p2)
print("Correct answer: [5.0, 0.0, 5.0]")
print("Yours:",poly.add(p1,p2))


p1=[3.0,1.0,2.0]
p2=[1.0,3.0]
print("\nTest add function using p1=",p1,"and p2=",p2)
print("Correct answer: [4.0, 4.0, 2.0]")
print("Yours:",poly.add(p1,p2))

print("\nTest add function using p1=",p2,"and p2=",p1)
print("Correct answer: [4.0, 4.0, 2.0]")
print("Yours:",poly.add(p2,p1))



p1=[2.0,-1.0,3.0]
p2=[3.0,1.0,-3.0]
print("\nTest add function using p1=",p1,"and p2=",p2)
print("Correct answer: [5.0]")
print("Yours:",poly.add(p1,p2))
