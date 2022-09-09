from xmlrpc.client import Boolean
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
#from google.cloud import storage
from forms import ManualForm, CourseForm
import re
from os import path 

#PREINPUT_URL = 'https://storage.googleapis.com/pre-data-bucket/preInput.txt'
ABS_PATH = path.abspath(__file__)
DIR_PATH = path.dirname(ABS_PATH)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt'}

#"automatic-gamma-361715"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#@app.route('/upload', methods=['POST'])
#def upload_file():
#   dest = 'part-three.html'
#    uploaded_file = request.files['file']
#    if uploaded_file.filename != '':
#        uploaded_file.save(uploaded_file.filename)
#    return redirect(url_for('index'))

@app.route('/runGoodTest', methods=['GET', 'POST'])
def loadGoodInput():
   # load good input from file
   # return list of tuples
   good_input_fn = "preInput.txt"
   metals_input_fn = "preMetals.txt"

   (g,r) = loadInput(good_input_fn,metals_input_fn)

   return render_template('content.html', input=g, content=r) 


@app.route('/runMessyTest', methods=['GET', 'POST'])
def loadMessyInput():
   # load good input from file
   # return list of tuples
   good_input_fn = "testInput.txt"
   metals_input_fn = "preMetals.txt"

   (g,r) = loadInput(good_input_fn,metals_input_fn)

   return render_template('content.html', input=g, content=r) 

def loadInput(input,metals):
   # load good input from file
   # return list of tuples
   good_input_fn = input
   metals_input_fn = metals

   metals_path = path.join(DIR_PATH, metals_input_fn)
   transactions_path = path.join(DIR_PATH, good_input_fn)
   res = []
   good = []
   # read allowed metals file, store in list, and clean up
   with open(metals_path, "r") as mf:
        # used filter bc Python iterators are well known to be memory efficient.
        # Non-blank lines in a list removed via filter
        mLines = tuple(filter(None, (line.rstrip() for line in mf)))  

        # read file, store in list, and clean up
        with open(transactions_path, "r") as tf:
            # Non-blank lines in a list removed via filter
            gLines = tuple(filter(None, (line.rstrip() for line in tf))) 

            good = gLines
            res = translateGalactic(gLines,mLines)

            # write results file for downloading
            
            with open(path.join(DIR_PATH,UPLOAD_FOLDER,"results.txt"), "w") as rf: 
               try:
                  rf.write('\n'.join(res))                
               except:
                  rf.write('\n'.join(str(line) for line in res))

            rf.close()
                
            #print(lines)
            tf.close()


        mf.close()

   if res:
      good = ('\n'.join(str(line) for line in good))
      res = ('\n'.join(str(line) for line in res))
      return (good, res)
   else:
      return ()



@app.route('/display', methods = ['GET', 'POST'])
def display_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()   
        
    return render_template('content.html', content=content) 


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

@app.route('/customInput', methods=['GET', 'POST'])
def customInput():
    dest = 'part-two.html'
    select = request.form.get('input_select')
    print(select)
    if select =='Type input transactions manually' :
      return render_template(dest,selectionManual=select, opt1=True)
    else:
      return render_template(dest,selectionManual=select, opt2=True)


@app.route('/tool')
def secondPage():
   return render_template('part-two.html')

@app.route('/numeralTools')
def thirdPage():
   return render_template('part-three.html')

@app.route('/textAreaInput')


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

   return render_template(dest, result=result)
   

def isRoman_Helper(val:str) -> bool:
    ## check if tuple.count vs str.count vs iterate str time complexity
    ## check regex vs brute force pattern match
    
    # check if these make difference in time complexity:
    #thousand.. 'M{0,3}'
    #hundred.. '(C[MD]|D?C{0,3})' = (CM|CD|D?C{0,3})
    #ten.. '(X[CL]|L?X{0,3})' = (XC|XL|L?X{0,3})
    #digit.. '(I[VX]|V?I{0,3})' = (IX|IV|V?I{0,3})
    regexR = r"M{0,3}(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3})$"

    try:
        v = str(val).upper()
        return bool(re.match(regexR, v))
    except:
        #sys.exit("Invalid roman numeral: " + str(val))  
        return False


@app.route('/romanToArabic', methods=['POST'])
def romanToArabic():
   dest = 'part-three.html'
   val = request.form['num2']

   if not val:
      result = "Empty input. Try Again."
      return render_template(dest, result2=result)
   
   result = romanToArabic_Helper(val.upper())
   if result == -1:
      result=str(val.upper()) + "... Ooops! Invalid roman numeral. Try Again."
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
            if isRoman_Helper(entry[-1]) and entry[0:-2]: #check if empty of units
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
            if entry[-4] in mlines:
               print("\n YAY metal name : " + str(entry[-4]))

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
                
                if isRoman_Helper(getRoman):
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
                calc = romanToArabic_Helper("".join(calc))
            
            elif j<len(eval) and (str(eval[j]).lower() in mc):
                metal_name = str(eval[j]).lower()
                g_val = mc[metal_name][1]

                if all(k in t for k in g_val):
                    # Silver val (arabic) divide by
                    # units (arabic <- roman <- galaxy)
                    arg = romanToArabic_Helper("".join([t[x] for x in g_val]))
                    mc[metal_name] = int(mc[metal_name][0]) / int(arg)


                elif isRoman_Helper(mc[metal_name][1]):
                    # divide Silver val (arabic) by
                    # units (arabic <- roman)
                    ar = int(romanToArabic_Helper("".join(g_val)))
                    mc[metal_name] = int(mc[metal_name][0]) / int(ar)
                else:
                    #("m in none")
                    pass

                calc = [int(romanToArabic_Helper("".join(calc))) * mc[metal_name]]

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
      
@app.route('/arabicToRoman', methods=['POST'])
def arabicToRoman():
   dest = 'part-three.html'
   val = request.form['num3']

   if not val:
      result = "Empty input. Try Again."
      return render_template(dest, result2=result)
   
   result = arabicToRoman_Helper(val.upper())
   if result == -1:
      result = str(val.upper()) + " ... Ooops! Invalid arabic numeral. Try Again."
   else:
      result = str(val.upper()) + " = " + str(result)

   return render_template(dest, result3=result)

def arabicToRoman_Helper(x):
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





if __name__ == "__main__":
   app.run(host="127.0.0.1", port=8080, debug=True)
   #app.run(host="127.0.0.1", debug=True)




"""
BUCKET_PREDATA = "pre-data-bucket"
BUCKET_TESTGALAXY = "test-galaxy-bucket"
BLOB_PREINPUT = "preInput.txt"
BLOB_TESTINPUT = "testInput.txt"

def download_public_file(bucket_name, source_blob_name):
   #Downloads a public blob from the bucket.
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client.create_anonymous_client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    assert blob.exists()
   #convert to text
    data = blob.download_as_text()
    print("downloaded blob")
   #blob.download_as_string()
   #blob.download_as_text
   #return blob.download_as_text()
    return data
    


def list_buckets():
    #Lists all buckets.

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)

def OLDtranslateGalactic(rlines): 
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

"""

