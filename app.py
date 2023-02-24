from flask import Flask,render_template,request,jsonify
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
app = Flask(__name__)

@app.route('/',methods=['POST'])
def m():
    return render_template('index.html')

@app.route('/company_results',methods=['POST'])
def company_results():
    if request.method=='POST':
        company_name=request.form['company-name']
        base_url='https://www.linkedin.com/search/results/all/?keywords='
        company_linkedin_search_url=base_url+company_name
        return company_linkedin_search_url

if __name__=="__main__":
    app.run(host="0.0.0.0")
