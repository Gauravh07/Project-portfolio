import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: scale\n\
###########################################\
")

p=[4.0,5.0]
print("\nTest scale function using p(x)=",p,'with 1.0 scaling factor')
print("Correct answer: [4.0, 5.0]")
print("Yours:",poly.scale(p,1.0))

p=[4.0,5.0]
print("\nTest scale function using p(x)=",p,'with 0.5 scaling factor')
print("Correct answer: [2.0, 2.5]")
print("Yours:",poly.scale(p,0.5))

p=[2.0,-4.0,5.0]
print("\nTest scale function using p(x)=",p,'with 2.0 scaling factor')
print("Correct answer: [4.0, -8.0, 10.0]")
print("Yours:",poly.scale(p,2.0))


p=[2.0,-4.0,5.0]
print("\nTest scale function using p(x)=",p,'with 0.0 scaling factor')
print("Correct answer: [0.0]")
print("Yours: ",poly.scale(p,0.0))



