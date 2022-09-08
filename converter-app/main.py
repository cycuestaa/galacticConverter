from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import re


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/')
@app.route('/instructions')
def firstPage():
   return render_template('part-one.html')

@app.route('/tool')
def secondPage():
   return render_template('part-two.html')

@app.route('/romanTool')
def thirdPage():
   return render_template('part-three.html')

@app.route('/isRoman', methods=['POST'])
def isRoman():
   dest = 'part-three.html'
   val = request.form['num1']

   if not val:
      result = "Empty input. Try Again"
   elif isRoman_Helper(val):
      result=str(val.upper())+ " .... YAY! Valid."
   else:
      #sys.exit("Invalid roman numeral: " + str(val))
      # TO DO render alert  
      result=str(val.upper())+ " ... Oops. INVALID!"
   
   return render_template(dest, result1=result)

def isRoman_Helper(val:str) -> bool:
    ## check if tuple.count vs str.count vs iterate str time complexity
    ## check regex vs brute force pattern match
    
    # check if these make difference in time complexity:
    #thousand.. 'M{0,3}'
    #hundred.. '(C[MD]|D?C{0,3})' = (CM|CD|D?C{0,3})
    #ten.. '(X[CL]|L?X{0,3})' = (XC|XL|L?X{0,3})
    #digit.. '(I[VX]|V?I{0,3})' = (IX|IV|V?I{0,3})
   regexR = r"M{0,3}(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3})$"
   return bool(re.match(regexR, val.upper()))

@app.route('/romanToArabic', methods=['POST'])
def romanToArabic():
   dest = 'part-three.html'
   val = request.form['num2']

   if not val:
      result = "Empty input. Try Again."
      return render_template(dest, result2=result)
   
   result = romanToArabic_Helper(val.upper())
   if result == -1:
      result = "Invalid Roman numeral. Try Again."
   else:
      result = str(val.upper()) + " = " + str(result)

   return render_template(dest, result2=result)


def romanToArabic_Helper(s:str) -> int:
    # input: string of roman numerals . upper()
    # output: int

   if not isRoman_Helper(s):
      #print("\t Value is not a valid Roman numeral")
      return -1
        # TODO : ask user if they would like to fix

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
   else:
      return total
        

@app.route('/basic-template')
def basicTemplate():
   return render_template('basic-template.html')

@app.route('/calculate', methods=['POST'])
def calculate():
   dest = 'part-two.html'
   num1 = request.form['num1']
   num2 = request.form['num2']
   operation = request.form['operation']

   if operation == 'add':
      result = float(num1) + float(num2)
      return render_template(dest, result=result)

   elif operation == 'subtract':
      result = float(num1) - float(num2)
      return render_template(dest, result=result)

   elif operation == 'multiply':
      result = float(num1) * float(num2)
      return render_template(dest, result=result)

   elif operation == 'divide':
      result = float(num1) / float(num2)
      return render_template(dest, result=result)
   else:
      return render_template(dest)

@app.route('/calcManual', methods=['POST'])
def calcManual():
   dest = 'part-two.html'
   input = request.form['text1']
   #celsius = request.args.get("celsius", "")
   result = ""
   if not input:
      result = "TODO can't compute"
   
   elif '\n' in input:
      #gLines = tuple(filter(None, (line.rstrip() for line in input)))
      
      result = translateGalactic(tuple(gLines))
   
   else:
      result="TODO else"
      return render_template(dest)


   return render_template(dest, result=result)


# -----------------------------------------------------------------------
# -------------- TRANSLATE INTERGALACTIC INPUTS ---------------
# -----------------------------------------------------------------------

def translateGalactic(rlines): 
   # readS lines from input file as tuple
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
         if isRoman_Helper(entry[-1]) and entry[0:-2]: #check if empty of units
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

         if isRoman_Helper(inRoman) and entry[-2].isdigit():
               #print(inRoman)
               metalConvert[str(entry[-4]).lower()] = (int(entry[-2]) /(romanToArabic(inRoman)), inRoman)
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
                     
               eval = romanToArabic("".join(eval))
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
                     eval = int(romanToArabic("".join(eval))) * float(metalConvert[str(entry[4:-1][i]).lower()][0])  

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

   print("galaxyRoman: " + str(galaxyRoman))
   print("metalConvert: " + str(metalConvert))
   print("originalVals = " + str(originalVals))
   print("convertedVals = " + str(convertedVals))
   
   return results


# -----------------------------------------------------------------------
# --------------- CONVERSION HELPERS ----------------
# -----------------------------------------------------------------------
      
      
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





if __name__ == "__main__":
   app.run(host="127.0.0.1", port=8080, debug=True)

