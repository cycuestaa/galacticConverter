import os
import re

from ntpath import join
from os import path


#from convert import Convert

def main():
    x = """\n---------------------------------------------\n
    **** InterGalactic Trading Converter ****
    \n---------------------------------------------\n
    Welcome! \n"""

    print(x)
    
    galaxy_filename = input("\tTo begin, enter filename containing intergalatic units: ")

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
        galaxy_filename = "testInput.txt"

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
            
            res = translateGalactic(gLines,mLines)

            with open(os.path.join(directory_path,"results.txt"), "w") as rf: #write results file
                #rf.writelines("%s\n" % res)
                try:
                    rf.write('\n'.join(res))                
                except:
                    rf.write('\n'.join(str(line) for line in res))

            rf.close()
                
            #print(lines)
            tf.close()


        mf.close()
        

# -----------------------------------------------------------------------
# -------------- TRANSLATE INTERGALACTIC INPUTS ---------------
# -----------------------------------------------------------------------

def translateGalactic(rlines,mlines): 
    # readS lines from input file as tuple

    galaxyRoman = {} # intergalatic to Roman dict
    metalConvert = {} # metal to credits
    originalVals = []
    
    # --- CHECK TYPE OF ENTRY and validate --------
    for i in range(len(rlines)):
        entry = tuple(str(rlines[i]).split())
        # Build dict: unit conversion by Roman numeral
        if len(entry) < 3:
            continue

        if entry[-2] == "is" and not (str(entry[-1]).lower() == "credits"):
            if isRoman(entry[-1]) and entry[0:-2]: #check if empty of units
                galaxyRoman[(" ".join(entry[0:-2])).lower()] = entry[-1]

            elif entry[-1] in galaxyRoman.values():
                # value already exists in galaxyRoman
                continue
                
            else :
                #print("\n Error: Invalid roman units : " + str(entry) + " credits? = " + str(entry[-1]).lower())
                continue
        

        # Build dict: metal credit conversion
        # Store in metalConvert dict at metal: 
        elif isMetalCred(str(entry[-1]),entry[-2]) and isinstance(entry[-4],str):
            ## TODO validate metal_name in mlines
            getRoman = []
            creds = entry[0:-4]
            for i in range(len(entry[0:-4])):
                if str(entry[i]) in galaxyRoman:
                    # key is avail in galaxyRoma
                    getRoman.append(galaxyRoman[entry[i]])
                
                # if not, two options:
                # 1 - not yet added, might still be!
                # 2 - is invalid key
                else:
                    getRoman = entry[0:-4]
                    break

            if entry[-2].isdigit() and isinstance(getRoman, tuple):
                metalConvert[str(entry[-4]).lower()] = (int(entry[-2]), getRoman)
            elif entry[-2].isdigit() and isinstance(getRoman, list):
                getRoman = ''.join(getRoman)
                
                if isRoman(getRoman):
                # metalConvert will contain {metal: (val, roman)}
                    metalConvert[str(entry[-4]).lower()] = (int(entry[-2]), getRoman)
            else:
                pass
                #("\n Error: Invalid roman units : " + str(entry))
                
        elif entry[-1] == "?":
            ## isEval should  be used so we can use it to convert to Galactic units referencing either unit or metal dicts
            
            if isEval(entry[:3]): # Eval Units
                originalVals.append(entry[3:-1])                    
                
            elif isEval(entry[:4]): # Eval Credits
                originalVals.append(entry[4:-1])  

            else:
                originalVals.append(())                
                #Eval question ignoring pattern check for how...is
                #check if only contains values from dicts
        else:
            #("\n Error: dunno: " + str(entry))
            pass

    #if galaxyRoman and metalConvert:
    return convertVals(originalVals,galaxyRoman,metalConvert)

def convertVals(ls,t,mc):
    res = []
    if ls and t and mc:
        for i in range(len(ls)):
            eval = ls[i]
            calc = []

            if not eval :
                res.append(())
                continue # loop next

            j = 0        
            while j<len(eval) and eval[j] in t:
                calc.append(t[eval[j]])
                j += 1
            
            if j==len(eval) and calc:
                calc = romanToArabic("".join(calc))
            
            elif j<len(eval) and (str(eval[j]).lower() in mc):
                metal_name = str(eval[j]).lower()
                g_val = mc[metal_name][1]

                if all(k in t for k in g_val):
                    # Silver val (arabic) divide by
                    # units (arabic <- roman <- galaxy)
                    arg = romanToArabic("".join([t[x] for x in g_val]))
                    mc[metal_name] = int(mc[metal_name][0]) / int(arg)


                elif isRoman(mc[metal_name][1]):
                    # divide Silver val (arabic) by
                    # units (arabic <- roman)
                    ar = int(romanToArabic("".join(g_val)))
                    mc[metal_name] = int(mc[metal_name][0]) / int(ar)
                else:
                    #("m in none")
                    pass

                calc = [int(romanToArabic("".join(calc))) * mc[metal_name]]

            res.append(calc)            

    return printNicely(ls,res)



def printNicely(og,cv):
    if isinstance(og,list) and isinstance(cv, list):
        a = list(map(' '.join, og))
        b = list(map(fixCredit, cv))
        new = []
        for i in range(len(b)):
            if not b[i]:
                new.append("I have no idea what you are talking about")
                continue
            
            try:
                int(b[i])
                new.append(str(a[i]) + ' is ' + str(b[i]))
            except:
                if isinstance(b[i],str):
                    new.append(str(a[i]) + ' is ' + b[i])
                    
        return new
    else:
        return ["I have no idea what you are talking about"]


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
        return ss
    except :
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

    try:
        v = str(val).upper()
        return bool(re.match(regexR, v))
    except:
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
                    #(5-1) or (10-1)
                    total += romanArabic[nxt] - romanArabic[curr] 
                    i += 2
            elif curr == "X" :
                # "X" can be subtracted from "L" and "C" only.
                if nxt == "L" or nxt == "C":
                    total += romanArabic[nxt] - romanArabic[curr] #(5-1) or (10-1)
                    i += 2
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
                pass
                
            total += romanArabic[curr]
            i += 1
        if total == 0:
            return -1
        
        return total
    else:
        #"\t Value is not a valid Roman numeral")
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


#Calculating the Time complexity



        
            



    






