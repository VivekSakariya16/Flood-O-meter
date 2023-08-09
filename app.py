from flask import Flask,request,render_template, url_for
import pickle
import pandas as pd

#defining the app
app=Flask(__name__)

#defining the models using pickle
pickle_in=open('model-final.pkl','rb')
classifier=pickle.load(pickle_in)

pickle_rg=open('hd_model.pkl','rb')
hd_regrr=pickle.load(pickle_rg)

pickle_rg_2=open('hf_model.pkl','rb')
hd_regrr_hf=pickle.load(pickle_rg_2)

#defining the app routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hd.html')
def hd():
    return render_template('hd.html')

@app.route('/fm.html')
def fm():
    return render_template('fm.html')

@app.route('/hf.html')
def hf():
    return render_template('hf.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

#handling clicks and making predictions 
@app.route('/fom-submit',methods=['POST','GET'])
def submit_fom():
   if request.method == 'POST':
      s=float(request.form['s'])
      m=float(request.form['m'])
      c=float(request.form['c'])
      prediction=classifier.predict([[c,s,m]])
      classification=0
      exp_area="area"
      if prediction == 0:
       classification=1
       exp_area="41.7932 - 19811837.41 meters "
      elif prediction == 1:
       classification=1.5
       exp_area="9467.55 - 517303.2 meters"
      else:
         classification=2
         exp_area="13472.46 - 1162598.06 meters"
   return render_template('result.html',predictionss=classification, exparea=exp_area) 
 
@app.route('/hd-submit',methods=['POST','GET'])
def submit_hd():
   if request.method == 'POST':
      a=float(request.form['a'])
      s=float(request.form['s'])
      m=float(request.form['m'])
      if s==1:
        s=0
      elif s==1.5:
        s=1
      else:
        s=2
      rg_prediction=hd_regrr.predict([[a,s,m]])
   return render_template('hdr.html',hd_pred=rg_prediction) 

 
@app.route('/hf-submit',methods=['POST','GET'])
def submit_hf():
   if request.method == 'POST':
      a=float(request.form['a'])
      hd=float(request.form['hd'])
      s=float(request.form['s'])
      m=float(request.form['m'])
      if s==1:
        s=0
      elif s==1.5:
        s=1
      else:
        s=2
      r_prediction=hd_regrr_hf.predict([[a,hd,s,m]])
   return render_template('hfr.html',hf_pred=r_prediction) 
 
if __name__ == '__main__':
    app.run(debug=True)