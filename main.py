import os
import re

from ntpath import join
from os import path


#from convert import Convert

def main():
    print("---------------------------------------------\n")
    print("**** InterGalactic Trading Converter ****")
    print("---------------------------------------------\n")

    
    galaxy_filename = input("Welcome!\nTo begin, enter filename containing intergalatic units: ")

    print("By default, this program validates transactions using our pre-compiled list of metals, and dirt!\n")

    metals_filename = input("If you would like to use your own list make sure each valid metal\nis on a new line, dont forget to include dirt!\nEnter filename: ")

    absolute_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(absolute_path)

    fn_good = "\nNice!! File found. Loading...\n"
    fn_bad = "\nOops... File not found. Make sure you have added it to this directory.\nFor now we'll use default: "
    
    print(absolute_path)
    print(directory_path)

    # Check input file is in path
    if os.path.isfile(galaxy_filename):
        print(fn_good)
    else:
        print(fn_bad + "preInput.txt\n")
        #galaxy_filename = "preInput.txt"
        galaxy_filename = "preInput.txt"

    # Check metals file is in path
    if os.path.isfile(metals_filename):
        print(fn_good)
    else:
        print(fn_bad + "preMetals.txt\n")
        metals_filename = "preMetals.txt"

    metals_path = os.path.join(directory_path, metals_filename)
    transactions_path = os.path.join(directory_path, galaxy_filename)


    # Read metals file
    with open(metals_path, "r") as mf: #read metals file
        # used filter bc Python iterators are well known to be memory efficient.
        mLines = tuple(filter(None, (line.rstrip() for line in mf)))   # Non-blank lines in a list
        print("\nMetals found: " + str(len(mLines)))

        # read file, store in list, and clean up
        with open(transactions_path, "r") as tf: #read transactions file
            # used filter bc Python iterators are well known to be memory efficient.
            gLines = tuple(filter(None, (line.rstrip() for line in tf)))   # Non-blank lines in a list

           # results_filename = input("\nGreat! Now enter a filename to save your results: ")
            
            res = translateGalactic(gLines)

            with open(os.path.join(directory_path,"results.txt"), "w") as rf: #write results file
                rf.writelines("%s\n" % res)

            rf.close()
                
            #print(lines)
            tf.close()


        mf.close()
        

# -----------------------------------------------------------------------
# -------------- TRANSLATE INTERGALACTIC INPUTS ---------------
# -----------------------------------------------------------------------

def translateGalactic(rlines): 
    # readS lines from input file as tuple

    galaxyRoman = {} # intergalatic to Roman dict
    metalConvert = {} # metal to credits
    originalVals = []
    
    # --- CHECK TYPE OF ENTRY and validate --------
    for i in range(len(rlines)):
        entry = tuple(str(rlines[i]).split())
        print("\n\t ... translateGalactic ::: " + str(entry) + "\n")
        # Build dict: unit conversion by Roman numeral
        if entry[-2] == "is" and not (str(entry[-1]).lower() == "credits"):
            if isRoman(entry[-1]) and entry[0:-2]: #check if empty of units
                galaxyRoman[(" ".join(entry[0:-2])).lower()] = entry[-1]

            elif entry[-1] in galaxyRoman.values():
                print("value already found in galaxyRoman")
                continue
                
            else :
                print("\n Error: Invalid roman units : " + str(entry) + " credits? = " + str(entry[-1]).lower())
        

        # Build dict: metal credit conversion
        # Store in metalConvert dict at metal: 
        elif isMetalCred(str(entry[-1]),entry[-2]) and isinstance(entry[-4],str):
            getRoman = []
            creds = entry[0:-4]
            print("\n Is metal cred : ")
            print(galaxyRoman)
            for i in range(len(entry[0:-4])):
                print(entry[i])

                
                if str(entry[i]) in galaxyRoman:
                    # key is avail in galaxyRoma
                    print("isMetalCred in galaxy: " + str(galaxyRoman[entry[i]]))
                    getRoman.append(galaxyRoman[entry[i]])
                
                # if not, two options:
                # 1 - not yet added, might still be!
                # 2 - is invalid key
                else:
                    print("else isMetalCred")
                    getRoman = entry[0:-4]
                    print(getRoman)

                    break


            print("type for getRoman : "+ str(type(getRoman)) + " = " + str(getRoman))
            if entry[-2].isdigit() and isinstance(getRoman, tuple):
                print("\t metalConvert will contain {metal: (val, [galaxy])}")
                metalConvert[str(entry[-4]).lower()] = (int(entry[-2]), getRoman)
            elif entry[-2].isdigit() and isinstance(getRoman, list):
                getRoman = ''.join(getRoman)
                print("getRoman : "+ str(getRoman))
                
                if isRoman(getRoman):
                # metalConvert will contain {metal: (true val, roman)}
                    metalConvert[str(entry[-4]).lower()] = (int(entry[-2]), getRoman)
                    
                    #(int(entry[-2]) /(romanToArabic(getRoman)), ''.join(getRoman))
                    print("yay add to metalConvert")
                else:
                    print("failed add to metalConver")
            else:
                print("\n Error: Invalid roman units : " + str(entry))
                
            
        elif entry[-1] == "?":
            ## isEval should  be used so we can use it to convert to Galactic units referencing either unit or metal dicts
            #eval = []
            
            if isEval(entry[:3]): # Eval units
                print("IS EVAL UNITS : " + str(entry[3:-1]))
                #evalUnits.append(entry[3:-1])
                #for i in range(len(entry[3:-1])):
                 #   if str(entry[3:-1][i].lower()) in galaxyRoman:
                  #      print(entry[3:-1][i].lower())
                   #     eval.append(galaxyRoman[entry[3:-1][i].lower()])
                    #else:
                        #save for later
                        #restVals.append(entry[3:-1][i])
                     #   print("... Error: Unable to evaluate " + str(entry[3:-1][i]) + " is not a valid unit\n")
                      #  break
                        
                #eval = romanToArabic("".join(eval))
                #if eval == -1 :
                 #   print("Error: invalid roman numeral")
                
                originalVals.append(entry[3:-1])
                #convertedVals.append(eval)  
                #results.append(" ".join(entry[3:-1]) + " is " + str(eval))
                    
                
            elif isEval(entry[:4]): # Eval Credits
                print("IS EVAL CREDITS : " + str(entry[4:-1]))
                #evalCreds.append(entry[4:-1])
                #for i in range(len(entry[4:-1])):   
                #    print(entry[4:-1][i])
                #    if str(entry[4:-1][i]).lower() in galaxyRoman:
                #        eval.append(galaxyRoman[entry[4:-1][i]])
                #        
                #    elif str(entry[4:-1][i]).lower() in metalConvert:
                #        eval = int(romanToArabic("".join(eval))) * float(metalConvert[str(entry[4:-1][i]).lower()][0])  

                #    else:
                 #       print("unknown")

                #if eval.is_integer():
                 #   eval = int(eval)
                #else:
                 #   print("Error: hard to have fractional credits")

                originalVals.append(entry[4:-1])  
                #convertedVals.append(eval)
                #results.append(" ".join(entry[4:-1]) + " is " + str(eval)+ " Credits")
            

            else:
                print("/nno match in eval/n")
                originalVals.append(())                
                #Eval question ignoring pattern check for how...is
                #check if only contains values from dicts

        else:
            print("\n Error: dunno: " + str(entry))

        print("galaxyRoman: " + str(galaxyRoman))
        print("metalConvert: " + str(metalConvert))
        #print("originalVals = " + str(originalVals))
    

    if galaxyRoman and metalConvert:
        return convertVals(originalVals,galaxyRoman,metalConvert)
    else:
        print("INSUFFICIENT")
    
    return originalVals

testOV = [('pish', 'tegj', 'glob', 'glob'), ('glob', 'prok', 'Silver')]
testGR = {'glob': 'I', 'prok': 'V', 'pish': 'X', 'tegj': 'L'}
def convertVals(ls,t,mc):
    res = []
    if ls:
        print("\n convertVals IN ORIGINAL VALS")
        print(ls)
        print(t)
        print(mc)
        

        for i in range(len(ls)):
            print("\n\n" + str(i) + " of " + str(len(ls)))
            calc = []
            eval = ls[i]

            if not eval :
                print("curr eval is empty")
                res.append(())
                continue
            else:
                print("curr eval : " + str(eval))

            j = 0        
            while j<len(eval) and eval[j] in t:
                #print(str(x[j]) + " in galaxy Roman")
                calc.append(t[eval[j]])
                j += 1
            
            if j==len(eval) and calc:
                calc = romanToArabic("".join(calc))
            
            elif j<len(eval) and (str(eval[j]).lower() in mc):
                print(str(eval[j]) + " in Metal convert")
                print(mc)
                metal_name = str(eval[j]).lower()
                print(mc[metal_name][1])
                g_val = mc[metal_name][1]

                if all(k in t for k in g_val):
                    print("m in galaxy, now convert")
                    # divide Silver val (arabic) by
                    # units (arabic <- roman <- galaxy)
                    arg = romanToArabic("".join([t[x] for x in g_val]))
                    mc[metal_name] = int(mc[metal_name][0]) / int(arg)


                elif isRoman(mc[metal_name][1]):
                    print("m is roman, now calc")
                    # divide Silver val (arabic) by
                    # units (arabic <- roman)
                    ar = int(romanToArabic("".join(g_val)))
                    mc[metal_name] = int(mc[metal_name][0]) / int(ar)
                else:
                    print("m in none")

                print("eval : " + str(eval))
                print("calc : " + str(calc))
                print("type mc[metal_name] : " + str(mc[metal_name]))
                print("int(romanToArabic(.join(calc[:-1]))) = " + str(int(romanToArabic("".join(calc)))))
                cc = (calc)
                print("cc = " + str(cc))
                calc = [int(romanToArabic("".join(calc))) * mc[metal_name]]
            else:
                print("duno duno")

            print("calc eval = " + str(calc))  
            res.append(calc)
            

    else:
        print("ORIGINAL VALS EMTPY")


        
    #print("galaxyRoman: " + str(galaxyRoman))
    #print("metalConvert: " + str(metalConvert))
    #print("originalVals = " + str(originalVals))
    print("\tconvertedVals = " + str(res))

    printNicely(ls,res)
    #final = list(map(' '.join, ls) + " is ")


def printNicely(og,cv):
    print(type(og))
    print(type(cv))
    if isinstance(og,list) and isinstance(cv, list):
        a = list(map(' '.join, og))
        b = list(map(fixCredit, cv))
        new = []
        for i in range(len(b)):
            if not b[i]:
                new.append("I have no idea what you are talking about")
                continue
            
            try:
                isinstance(b[i],str)
                new.append(str(a[i]) + ' is ' + b[i])
            except:
                int(b[i])
                new.append(str(a[i]) + ' is ' + str(b[i]))
                    

        print("printing nicely...")
    print("/n printedNicely = /n" + str(new))



def fixCredit(s):
    # input: string
    if not isinstance(s,list) or not s:
        return s
    ss = str(s[0])
    try : 
        ss = float(s[0])
        if ss == float(1):
            ss = str(ss) + " Credit" 
        elif float(s[0]).is_integer():
            ss = str(int(ss)) + " Credits"
        else:
            ss = str(ss) + " Credits"
        print("fixCredit = " + ss)
        return ss


        
    except :
        print("fixCredit except = " + str(s))
        return s


# -----------------------------------------------------------------------
# --------------- CONVERSION HELPERS ----------------
# -----------------------------------------------------------------------

def isRoman(val):
    ## check if tuple.count vs str.count vs iterate str time complexity
    ## check regex vs brute force pattern match
    
    # check if these make difference in time complexity:
    #thousand.. 'M{0,3}'
    #hundred.. '(C[MD]|D?C{0,3})' = (CM|CD|D?C{0,3})
    #ten.. '(X[CL]|L?X{0,3})' = (XC|XL|L?X{0,3})
    #digit.. '(I[VX]|V?I{0,3})' = (IX|IV|V?I{0,3})
    regexR = r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"

    if bool(re.match(regexR, str(val).upper())):
        return True
    else:
        #sys.exit("Invalid roman numeral: " + str(val))  
        return False

def romanToArabic(s):
    # input: string of roman numerals
    # output: int

    if isRoman(s):
        romanArabic = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        eval = tuple(s)
        total = 0
        i = 0
        while i < (len(eval)):
            curr = eval[i]

            if i+1 == len(eval):
                nxt = ''
            else:
                nxt = eval[i+1]

            if curr == "I" :
            # "I" can be subtracted from "V" and "X" only.
                if nxt == "V" or nxt == "X":
                    total += romanArabic[nxt] - romanArabic[curr] #(5-1) or (10-1)
                    i += 2
                else:
                    total += romanArabic[curr]
                    i += 1
            elif curr == "X" :
                # "X" can be subtracted from "L" and "C" only.
                if nxt == "L" or nxt == "C":
                    total += romanArabic[nxt] - romanArabic[curr] #(5-1) or (10-1)
                    i += 2
                else:
                    total += romanArabic[curr]
                    i += 1
            elif curr == "C" :
                # "C" can be subtracted from "D" and "M" only.
                if nxt == "D" or nxt == "M":
                    total += romanArabic[nxt] - romanArabic[curr] #(5-1) or (10-1)
                    i += 2
                else:
                    total += romanArabic[curr]
                    i += 1
            else:
                #"V", "L", and "D" can never be subtracted
                total += romanArabic[curr]
                i += 1
        if total == 0:
            return -1
        
        return total
    else:
        print("\t Value is not a valid Roman numeral")
        return -1
        # TODO : ask user if they would like to fix
        
        
def arabicToRoman(x):
        # chose to use ** nstead of math.pow() bc it is faster
        # https://chrissardegna.com/blog/python-expontentiation-performance/
        
        #romanArabic = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        arabicVals = (1000,900,500,400,100,90,50,40,10,9,5,4,1)
        romanVals = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')

        val = x
        rv = []
        if str(val).isdigit():
            for i in range(len(arabicVals)):
                if arabicVals[i] > int(val):
                    continue  # loop until <= key

                rem = int(val) // arabicVals[i]  # use remainder
                if not rem:
                    continue # if 0, skip

                rv.append(romanVals[i] * rem)
                
                val = int(val) - (arabicVals[i] * rem)
                if not val:
                    break # leave loop 

            return ("".join(rv))
        else:
            return "Invalid input"



# -----------------------------------------------------------------------
# --------------- VALIDATE METALS ----------------
# -----------------------------------------------------------------------

def allowedMetals():
    return ["Silver", "Gold", "Iron", "Dirt"]

def isMetal(val):
    if str(val.lower()) in allowedMetals().lower():
        return True
    else:
        return False


def isMetalCred(cred, val):
    if (str(cred).lower()) == "credits" and str(val).isdigit(): #and eq == "is"
        #TODO: check if metal is in metals list 
        #TODO: build metal list
        return True
    return False
               

def isEval(val):
    if (len(val) == 3 and " ".join(val).lower() == "how much is") or (len(val) == 4 and " ".join(val).lower() == "how many credits is"):
        return True
    else:
        ## iterate thru, check if all values are in galaxyRoman or metalConvert

        # else
        return False





main()

def getKeyVal(list,dict):
    #for key in dict 
    keys = [dict[x] for x in list]

    print(keys)
#Calculating the Time complexity



        
            



    






