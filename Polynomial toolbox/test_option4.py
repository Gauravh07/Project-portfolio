import polynomial as poly


print("\n\
###########################################\n\
#### Test for the function: evaluate\n\
###########################################\
")

p=[4.5,5.0]
print("\nTest evaluate function using p(x)=",p,'at x=3.5')
print("Correct answer: 22.0")
print("Yours:",poly.evaluate(p,3.5))

p=[-2.0,1.0,2.0,0.0,3.0]
print("\nTest evaluate function using p(x)=",p,'at x=-5')
print("Correct answer: 1918.0")
print("Yours:",poly.evaluate(p,-5))

p=[2.0]
print("\nTest evaluate function using p(x)=",p,'at x=10')
print("Correct answer: 2.0")
print("Yours:",poly.evaluate(p,10))
