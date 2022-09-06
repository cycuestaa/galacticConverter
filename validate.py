import re


class Validator():
    # Class to validate input
    # used for roman numerals and allowed metals (+dirt)

    def allowedMetals():
        return ["Silver", "Gold", "Iron"]

    def isRoman(val):
            ## check if tuple.count vs str.count vs iterate str time complexity
            ## check regex vs brute force pattern match
            
            # check if these make difference in time complexity:
            #thousand.. 'M{0,3}'
            #hundred.. '(C[MD]|D?C{0,3})' = (CM|CD|D?C{0,3})
            #ten.. '(X[CL]|L?X{0,3})' = (XC|XL|L?X{0,3})
            #digit.. '(I[VX]|V?I{0,3})' = (IX|IV|V?I{0,3})

            regexR = r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"

            if bool(re.match(regexR, val.upper())):
                return True
            else:
                #sys.exit("Invalid roman numeral: " + str(val))  
                return False

    def isMetal(val):  

        return True
