# new file

from ntpath import join
import os
import sys
import time
import re

from validate import Validator
from convert import Converter


def isMetalCred(cred, val, eq, unit):
    if (cred) == "credits" and str(val).isdigit() and eq == "is" :
        if (unit == "Silver" or unit == "Gold" or unit == "Iron" or unit == "Dirt"):
            return True
        print("fix metal")
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



def translateGalactic(rlines): #read lines from input file as tuple
    calcRoman = Converter.calcRoman()
    isRoman = Validator.isRoman()
    
    galaxyRoman = {}
    metalConvert = {}
    originalVals = []
    convertedVals = []
    results = []
    
    # --- CHECK TYPE OF ENTRY and validate --------
    for i in range(len(rlines)):
        entry = tuple(str(rlines[i]).split())

        # Build dict: unit conversion by Roman numeral
        if entry[-2] == "is":
            if isRoman(entry[-1]) and entry[0:-2]: #check if empty of units
                galaxyRoman[(" ".join(entry[0:-2])).lower()] = entry[-1]

            else:
                print("\n Error: Invalid roman units : " + str(entry))
        

        # Build dict: metal credit conversion
        # Store in metalConvert dict at metal: (value in arabic)
        elif isMetalCred(str(entry[-1]).lower(),entry[-2],entry[-3],entry[-4]):
            inRoman = []
            for i in range(len(entry[0:-4])):
                if entry[i] in galaxyRoman:
                    inRoman.append(galaxyRoman[entry[i]])
            inRoman = ''.join(inRoman) 

            if isRoman(inRoman) and entry[-2].isdigit():
                print(inRoman)
                metalConvert[str(entry[-4]).lower()] = int(entry[-2]) /(calcRoman(inRoman))
            else:
                print("\n Error: Invalid roman units : " + str(entry))
            
        elif entry[-1] == "?":
            ## isEval should  be used so we can use it to convert to Galactic units referencing either unit or metal dicts
            eval = []
            if isEval(entry[:3]): # Eval units
                for i in range(len(entry[3:-1])):
                    if str(entry[3:-1][i].lower()) in galaxyRoman:
                        eval.append(galaxyRoman[entry[3:-1][i].lower()])
                    else:
                        print("... Error: Unable to evaluate " + str(entry[3:-1][i]) + " is not a valid unit\n")
                        break
                        
                eval = calcRoman("".join(eval))
                if eval == -1 :
                    print("Error: invalid roman numeral")
                
        
                originalVals.append([entry[3:-1]])
                convertedVals.append(eval)  
                results.append(" ".join(entry[3:-1]) + " is " + str(eval))
                

                    
                
            elif isEval(entry[:4]): # Eval Credits
                for i in range(len(entry[4:-1])):
                    if str(entry[4:-1][i]).lower() in galaxyRoman:
                        eval.append(galaxyRoman[entry[4:-1][i]])
                        
                    elif str(entry[4:-1][i]).lower() in metalConvert:
                        eval = int(calcRoman("".join(eval))) * float(metalConvert[str(entry[4:-1][i]).lower()])  

                    else:
                        print("unknown")

                if eval.is_integer():
                    eval = int(eval)
                else:
                    print("Error: hard to have fractional credits")

                originalVals.append(entry[4:-1])  
                convertedVals.append(eval)
                results.append(" ".join(entry[4:-1]) + " is " + str(eval)+ " Credits")
            
            

            else:
                originalVals.append([])
                convertedVals.append(-1)
                results.append("I have no idea what you are talking about")
                

                #Eval question ignoring pattern check for how...is
                #check if only contains values from dicts

        else:
            print("\n Error: dunno: " + str(entry))

    print("originalVals = " + str(originalVals))
    print("convertedVals = " + str(convertedVals))
    
    return results

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

            results_filename = input("\nGreat! Now enter a filename to save your results: ")
            
            res = translateGalactic(gLines)

            with open(os.path.join(directory_path,results_filename), "w") as rf: #write results file
                rf.write("\n".join(res))

            rf.close()
                
            #print(lines)
            tf.close()


        mf.close()
        


main()


#Calculating the Time complexity



        
            



    






