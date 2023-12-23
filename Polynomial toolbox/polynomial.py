###############################
# Team members- Please enter your names here
# Name1:Gaurav Hareesh
# Name2:Anshuman Deodhar
###############################


def display_menu():
    """Display the list of polynomial available tools"""
    print("1-Insert; 2-Remove; 3-Info; 4-Evaluate; 5-Scaling; 6-Derive; 7-Integrate")
    print("8-Summation; 9-Subtract; 10-Multiply; 11-Divide")


def display_list(list_poly):
    # the instruction below is just a placeholder
    # you must remove the instruction and modify/complete this function
    list_poly = list_poly



#option 1
def get_polynomial():
    Degree= int(input("Degree of polynomial? "))
    list = [0] 
    list=list*(Degree+1)
    x=""   
    for i in range(0,Degree+1):
        n = float(input("Enter coef. of x^{%s}"%(i)))
        list[i] = n
    p=str(n)    
    x=x+p
    return list
def get_expression(coefficients):
    poly_string = ""

    if len(coefficients) == 0:
        return "0.0"
    all_zeros = True
    for coefficient in coefficients:
        if coefficient != 0.0:
            all_zeros = False
            break
    if all_zeros:
        return "0.0"
    for i in range(len(coefficients)):
        if coefficients[i] == 0:
            continue
        elif i == 0:
            poly_string = poly_string+str(coefficients[i])
        elif i == 1:
            if coefficients[i] == 1:
                poly_string += "x"
            else:
                poly_string = poly_string+str(coefficients[i]) + "x"
        else:
            if coefficients[i] == 1:
                poly_string = poly_string+"x^" + str(i)
            else:
                poly_string = poly_string+str(coefficients[i]) + "x^" + str(i)

        if i != len(coefficients) - 1:
            poly_string = poly_string+" + "

    return poly_string
def display_list(list_poly):
    for i in range(len(list_poly)):
        print(i+1, ":", get_expression(list_poly[i]))
        





#option 3
def info(t):
    degree = len(t) - 1
    is_even = True
    is_odd = True
    
    for i in range(1, degree+1, 2):
        if t[i] != 0:
            is_even = False
            break
    
    for i in range(0, degree+1, 2):
        if t[i] != 0:
            is_odd = False
            break
    
    if is_even and is_odd == False:
        return "Degree is %s and it is an even." % degree
    elif is_odd and is_even == False:
        if t[0] == t[2] == t[4] == 0.0:
            degree=degree-1
            return "Degree is %s and it is an odd." % degree
        else:
            return "Degree is %s." % degree
    else:
        return "Degree is %s." % degree

       
    
#Option 4:
def evaluate(p, x):
    evaluated_polynomial = p[0]
    for i in range(1, len(p)):
        evaluated_polynomial =evaluated_polynomial+ p[i] * x ** i
    return evaluated_polynomial





#Option 5:
def scale(polynomial, scalingfactor):
    scaledpolynomial = [0] * len(polynomial)
    for i in range(len(polynomial)):
        scaledpolynomial[i] = polynomial[i] * scalingfactor
    return scaledpolynomial       

#Option 6:
def derive(polynomial):
    if len(polynomial) < 2:
        return [0.0]
    derived_polynomial = [0.0] * (len(polynomial) - 1)
    for i in range(1, len(polynomial)):
        derived_polynomial[i - 1] = i * polynomial[i]
    return derived_polynomial

#Option 7:
def integrate(polynomial, lower_bound, upper_bound):
    antiderivative = [0.0] * (len(polynomial) + 1)
    for i in range(len(polynomial)):
        antiderivative[i+1] = polynomial[i] / (i+1)
    integral = evaluate(antiderivative, upper_bound) - evaluate(antiderivative, lower_bound)
    return integral


#Option 8:
def add(firstpolynomial, secondpolynomial):
    len1 = len(firstpolynomial)
    len2 = len(secondpolynomial)
    newpolynomial = [0.0] * (len1+len2-1)
    for i in range(len1):
        newpolynomial[i] =newpolynomial[i]+firstpolynomial[i]
    for i in range(len2):
        newpolynomial[i] =newpolynomial[i]+secondpolynomial[i]
    while len(newpolynomial) > 1 and newpolynomial[-1] == 0.0:
        newpolynomial = newpolynomial[:-1]
    return newpolynomial



#option 9
def subtract(p1, p2):
    n1, n2 = len(p1), len(p2)
    if n1 < n2:
        p1 = p1+[0.0] * (n2 - n1)
    elif n2 < n1:
        p2 =p2+ [0.0] * (n1 - n2)
   
    result = [0.0] * n1
    for i in range(n1):
        result[i] = p1[i] - p2[i]
   
    zero = True
    for coeff in result:
        if coeff != 0.0:
            zero = False
            break
    if zero:
        return [0.0]
    else:
        return result


#option 10
def multiply(p1, p2):
    p = [0.0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            p[i+j] =   p[i+j]+p1[i] * p2[j]
    all_zeros = True
    for val in p:
        if val != 0.0:
            all_zeros = False
            break
    if all_zeros:
        return [0.0]
    else:
        return p

    
