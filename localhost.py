from flask import Flask, redirect, url_for, request, render_template
from apyori import apriori
import pandas as pd

app = Flask(__name__)

def Algorithm(d):
    size=d.shape
    records = []
    for i in range(0, size[0]):
        records.append([str(d.values[i,j]) for j in range(0, size[1])])
    association_rules = apriori(records, min_support=0.0063, min_confidence=0.20, min_lift=3, min_length=2)
    association_results = list(association_rules)
    res1 = []
    count = 0
    for item in association_results:
        if count == 0:
            res = "=>"
            res1.append(res)
        count+=1
        
        pair = item[0]
        items = [x for x in pair]
        res = "====>"
        res1.append(res)
        res = "Rule: " + items[0] + " -> " + items[1]
        res1.append(res)

        #second index of the inner list
        res = "Support => " + str(item[1])
        res1.append(res)
    
        #third index of the list located at 0th
        #of the third index of the inner list
    
        res = "Confidence => " + str(item[2][0][2])
        res1.append(res)
        res = "Lift => " + str(item[2][0][3])
        res1.append(res)
        res = "==>"
        res1.append(res)

        if count == 3:
            res = "===>"
            res1.append(res)
            count = 0
        
    return render_template('result.html', result=res1)
        

@app.route('/locomachine',methods = ['POST', 'GET'])
def locomachine():
    if request.method == "POST":
        data = request.files["file"]
        df = pd.read_csv(data, header=None)
        return Algorithm(df)
    


@app.route('/preloaded',methods = ['POST', 'GET'])
def preloaded():
    if request.method == "POST":
        dataset = request.form["predata"]
        if dataset == '1000':
            df=pd.read_csv("Datasets\\1000-out1.csv", header=None)
        elif dataset == '5000':
            df=pd.read_csv("Datasets\\5000-out1.csv", header=None)
        elif dataset == '20000':
            df=pd.read_csv("Datasets\\20000-out1.csv", header=None)
        elif dataset == '75000':
            df=pd.read_csv("Dataset\\75000-out1.csv", header=None)
    return Algorithm(df)

if __name__ == '__main__':
   app.run(debug = False)