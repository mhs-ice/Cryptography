def main():
    p=int(input("Enter the value of p : "))
    a=int(input("Enter the value of a : "))
    b=int(input("Enter the value of b : "))
    g_input=(input("Enter the value of G (x,y) : "))
    g=tuple(map(int, g_input.split(',')))

    alpha=int(input("enter the private key of A : "))
    pa=point_multiply(alpha, g , a , p)
    print("alice public key : ", pa)

    beta=int(input("enter bobs privarte key beta : "))
    pb=point_multiply(beta, g, a, p)
    print("Bobs public key : ", pb)

    alice_shared_key=point_multiply(alpha, pb, a , p)
    bob_shared_key=point_multiply(beta, pa, a , p)

    print("Alice shared key :", alice_shared_key)
    print("Bobs shared key :", bob_shared_key)
    print("Key exhange successful" if alice_shared_key==bob_shared_key else "key exchange failed")


    pm=get_valid_point(p,a,b)
    c1=point_multiply(alpha,g,a,p)
    alpha_pb=point_multiply(alpha,pb,a,p)
    c2=point_add(pm,alpha_pb,a,p)

    ciphertext=(c1,c2)
    print("Encrypted: ", ciphertext)

    beta_c1=point_multiply(beta,c1,a,p)
    beta_c1_inv=(beta_c1[0], (-beta_c1[1])%p)
    decrypted=point_add(c2, beta_c1_inv,a,p)
    print("decrypted:", decrypted)





def point_add(P, Q, a , p):
    if P=='O':
        return Q
    if Q=='O':
        return P
    
    x1,y1=P
    x2,y2=Q

    if x1==x2 and (y1+y2)%p==0:
        return 'O'
    
    if P!=Q:
        m= (y2-y1)*pow((x2-x1), -1, p)%p
    else:
        m=((3*x1*x1)+a)*pow(2*y1, -1, p)%p

    xr=(m**2-x1-x2)%p 
    yr= (m*(x1-xr)-y1)%p

    return xr,yr

def point_multiply(k, point, a , p):
    result="O"
    addend = point

    while k:
        if k & 1:
            result=point_add(result, addend, a, p)
        addend=point_add(addend, addend, a, p)
        k>>=1

    return result

def is_point_on_curve(point, a , b , p):
    if point=="O":
        return True
    x,y=point

    return y**2%p==(x**3+a*x+b)%p

def get_valid_point(p,a,b):
    while True:
        pm=input("Enter the msg point:")
        x,y=tuple(map(int, pm.split(",")))

        if is_point_on_curve((x,y), a,b,p):
            return x,y
        else:
            print('Not in the curve')


if __name__=="__main__":
    main()

