from flask import Flask,render_template,request,session
from pymongo import MongoClient

cluster=MongoClient("127.0.0.1:27017")

db=cluster['healthrecords']
#collection for login details
patients=db['patients']
records=db["records"]
admin=db['admin']

app = Flask(__name__)
app.secret_key="akhil"

@app.route("/")
def home():
  return render_template("welcome.html")

@app.route("/doclogin")
def doclogin():
  return render_template("doctorlogin.html")

@app.route("/docsignup")
def docsignup():
  return render_template("docsignup.html")

@app.route("/adminhome")
def adminhome():
  return render_template("admin.html")

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/signup")
def signup():
  return render_template("signup123.html")

@app.route("/forgot")
def forgot():
  return render_template("forgot.html")

@app.route("/start")
def start():
  return render_template("start1.html")

@app.route("/home")
def home2():
  return render_template("home2.html")

@app.route("/records")
def records1():
  return render_template("records.html")

@app.route("/patient records")
def patient():
  user=records.find_one({"email":session['email']})
  return render_template("paicent.html",data=user)

@app.route("/services")
def services():
  return render_template("services.html")

@app.route("/university")
def university():
    return render_template("university.html")

@app.route("/con")
def con():
  return render_template("cons.html")

@app.route("/fitness")
def fitness():
  return render_template("fitness.html")

@app.route("/weg")
def weg():
    return render_template("weg.html")

@app.route("/loss")
def loss():
    return render_template("loss.html")

@app.route("/gain")
def gain():
    return render_template("gain.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html") 
  


   
#login details store
@app.route("/loginuser",methods=['post'])
def loginusers():
  a=request.form.get("email")
  b=request.form.get("password")
  user=patients.find_one({"email":a})
  if(user):
    if user['password']==b:
      session['email']=a
      print(session['email'])
      return render_template("start1.html",status="Logged in successfully",data=a)
  return render_template("login.html",status="invalid credentials")

#signup details data base    
@app.route("/registeruser",methods=["post"])
def signinuser():
  d=request.form.get("name")
  e=request.form.get("email")
  f=request.form.get("phone")
  h=request.form.get("gender")
  i=request.form.get("age")
  j=request.form.get("address")
  k=request.form.get("password")
  
  user=patients.find_one({"email":e })
  if(user):
    return render_template("signup123.html",status="email already exist")
  patients.insert_one({"name":d,"email":e,"phone":f,"gender":h,"age":i,"address":j,"password":k})
  return render_template("login.html")

#records data store
@app.route("/records", methods=['POST'])
def recordsuser():
    if 'email' not in session:
        return render_template("login.html", status="Please log in first.")

    # Fetch data from the form
    a = session['email']  # Use the session email to link the records
    b = request.form.get("name")
    c = request.form.get("phone")
    d = request.form.get("dob")
    e = request.form.get("gender")
    f = request.form.get("address")
    g = request.form.get("blood-type")
    h = request.form.get("height")
    i = request.form.get("weight")
    j = request.form.get("past-operations-number")
    k = request.form.get("operation-details")
    l = request.form.get("complications")
    m = request.form.get("sugar-level")
    n = request.form.get("bp-systolic")
    o = request.form.get("bp-diastolic")
    p = request.form.get("message")

    # Store the record in the database
    records.insert_one({
        "email": a,  # Associate record with patient email
        "name": b,
        "phone": c,
        "dob": d,
        "gender": e,
        "address": f,
        "blood-type": g,
        "height": h,
        "weight": i,
        "past-operations-number": j,
        "operation-details": k,
        "complications": l,
        "sugar-level": m,
        "bp-systolic": n,
        "bp-diastolic": o,
        "message": p
    })

    return render_template("home2.html", status="Submission successful")


#doc sign up
@app.route("/signupdata",methods=['post'])
def doctorsignup():
  a=request.form.get("name")
  b=request.form.get("email")
  c=request.form.get("hospitalname")
  d=request.form.get("password")
  
  user=admin.find_one({"email":b})
  if(user):
    return render_template("docsignup.html",status="email already exist")
  admin.insert_one({"name":a,"email":b,"hospitaname":c,"password":d})
  return render_template("doctorlogin.html")


#admin login page
@app.route("/doctorlogin",methods=['post'])
def doctorlogin():
  a=request.form.get("email")
  b=request.form.get("password")
  user=admin.find_one({"email":a})
  if user['password']==b:
    return render_template("admin.html")
  return render_template("doctorlogin.html",status="Invalid credentials")

#view records
@app.route("/patient records")
def view_records():
    if 'email' not in session:
        return render_template("login.html", status="Please log in first.")

    # Fetch records from the database linked to the logged-in patient
    user_records = records.find({"email": session['email']})
    return render_template("paicent.html", records=user_records)
  
  
@app.route("/admincard")
def admincard():
    query = request.args.get('query')
    if query:
        # Search by name or email (case-insensitive)
        search_results = records.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"email": {"$regex": query, "$options": "i"}}
            ]
        })
    else:
        search_results = records.find()
    
    return render_template("123.html", records=search_results)




if __name__ == "__main__":
  app.run(port=3600,debug=True)
  app.run(port=4666,debug=True)
