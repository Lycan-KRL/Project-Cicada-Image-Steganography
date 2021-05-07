def divPos(n, d):
    q = 0
    r = n 

    while (r >= d):
        q += 1
        r -= d

    return q

def divNeg(n, d):
    q = 0
    r = n 

    while (r < 0):
        q -= 1
        r += d

    return q

def euclid(x, y):
    if x <= 0 or y <= 0:
        print("Give positive numbers!")
    else:
        if (y > x):
            t = x
            x = y
            y = t
        
        r = y % x

        while (r != 0):
            y = x
            x = r 
            r = y % x

        return x

def d2b(d, b):
    x = d
    str1 = ""
    while x > 0:
        str1 += str(x % b) + " "
        x = int( x / b )

    str1 = str1[::-1]
    print(str1, end="\n\n")

def b2d(rep, b):
    x = 0
    bits = 0
    power = 0

    temp = rep
    while temp != 0:
        bits += 1
        temp = int( temp / 10 )

    while bits >= 0:
        x += (rep % 10) * pow(b, power)
        power += 1
        rep = int( rep / 10 )
        bits -= 1

    return x


def remainder(n, d, q):
    # n = qd + r
    # r = n - qd
    return (n - (q * d))


def main():
    while (1):
        print("Euclid GCD (1)\nDiv/Mod (2)\nDec2Base(3)\nBase2Dec(4)\n")
        print("Enter Option: ", end="")
        option = int( input() )

        if option == 1:
            print("Euclid GCD\n")
            print("Enter lo: ", end="")
            lo = int( input() )
            print("Enter hi: ", end="")
            hi = int( input() )

            print("GCD = " + str( euclid(lo, hi) ), end='\n\n')
        elif option == 2:
            print("Div/Mod\n")
            print("Enter quotient: ", end="")
            num = int( input() )
            print("Enter divisor: ", end="")
            div = int( input() )

            q = 0

            if (num < 0):
                q = divNeg(num, div)
            else:
                q = divPos(num, div)

            r = remainder(num, div, q)

            print("Quotient  = " + str(q) + "\nRemainder = " + str(r), end='\n\n')
        elif option == 3:
            print("Dec2Base\n")
            print("Enter decimal: ", end="")
            dec = int( input() )
            print("Enter base: ", end="")
            base = int( input() )

            d2b(dec, base)
        elif option == 4:
            print("Base2Dec\n")
            print("Enter representation: ", end="")
            rep = int( input() )
            print("Enter base: ", end="")
            base = int( input() )

            dec = b2d(rep, base)
            print("Decimal Result = " + str(dec), end="\n\n")
        else: 
            print("Invalid Answer", end='\n\n')

if __name__ == "__main__": main()