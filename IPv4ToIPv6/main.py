import math

eingabe = input("Ihre Eingabe? ")
ipv4 = eingabe.split('.')

nubs = []

def gethexvalue(number):
    hexnumber = '0';
    if number == 10:
        hexnumber = 'A';
    elif number == 11:
        hexnumber = 'B'
    elif number == 12:
        hexnumber = 'C'
    elif number == 13:
        hexnumber = 'D'
    elif number == 14:
        hexnumber = 'E' 
    elif number == 15:
        hexnumber = 'F'
    else:
        hexnumber = str(number);
    return hexnumber 

def combindepath(hex1,hex2):
    nubs.append(hex1 + hex2)

 
for i in ipv4:
    firstpart = int(int(i) / 16)
    secondpart = int(i) % 16
    hex1 = gethexvalue(firstpart)
    hex2 = gethexvalue(secondpart)
    combindepath(hex1,hex2)

ausgabe = ""

for i in nubs:
    ausgabe = ausgabe + i
    
print (ausgabe)