import pickle
from flask import Flask, request, render_template, jsonify
import numpy as np
app = Flask(__name__)

# load data and extract all the vectors
with open('Proposal_DeRecSITEmP.pkl', 'rb') as f:
    graduate_data = pickle.load(f)
list_backgrounds = sorted([background['Background'] for background in graduate_data]) #Background comes from the dataset
#We select data from graduate_data to display in each balise select of html
list_bornwar = sorted(set([background['BornWar'] for background in graduate_data]))
list_univtype = sorted(set([background['UniversityType'] for background in graduate_data]))
list_instloc = sorted(set([background['InstitutionLocation'] for background in graduate_data]))
list_schwar = sorted(set([background['SchoolWar'] for background in graduate_data]))
list_homepi = sorted(set([background['HomeEpidemic'] for background in graduate_data]))
list_degree = sorted(set([background['Degree'] for background in graduate_data]))
list_family = sorted(set([background['Family'] for background in graduate_data]))
list_polfam = sorted(set([background['PoliticianFam'] for background in graduate_data]))
list_admfam = sorted(set([background['AdminstrativeFam'] for background in graduate_data]))
list_comfam = sorted(set([background['CompanyFam'] for background in graduate_data]))
list_fat = sorted(set([background['Father'] for background in graduate_data]))
list_mot = sorted(set([background['Mother'] for background in graduate_data]))
graduatekey_list = [item['graduatekey'] for item in graduate_data] #graduatekey comes from the dataset

@app.route("/", methods=['GET', 'POST'])
def template_test():
    if request.method == 'POST':
        #We obtain all the inputs from the html form
        bw= request.form.get('BornWar')
        ut = request.form.get('UniversityType')
        il = request.form.get('InstitutionLocation')
        sw = request.form.get('SchoolWar')
        he = request.form.get('HomeEpidemic')
        dg = request.form.get('Degree')
        fa = request.form.get('Family')
        pfa = request.form.get('PoliticianFam')
        adfa = request.form.get('AdminstrativeFam')
        comfa = request.form.get('CompanyFam')
        Father = request.form.get('Father')
        Mother = request.form.get('Mother')
        #We precise the metric we are using
        selected_metric ='cosine'
        #We concatenate all the obtained inputs to make background variable
        background= bw +  " " + ut + " " + il + " " + sw + " " + he + " " + dg + " " + fa + " " + pfa + " " + adfa + " " + comfa + " " + Father + " " + Mother 
        selected_background = next(item for item in graduate_data if item['Background'] == background)
        similar_backgrounds = [graduate_data[i] for i in selected_background[selected_metric]]
        return render_template('index.html', similar_backgrounds=similar_backgrounds[:3]) #We return the three most similar backgrounds
    else:
        #This else will execute before cliquing on Recommender. It fills selects of html form
        return render_template('index.html',list_bornwar=list_bornwar,list_univtype=list_univtype,
        list_instloc=list_instloc,list_schwar=list_schwar,list_homepi=list_homepi,list_degree=list_degree,list_family =list_family,
        list_polfam=list_polfam,list_admfam=list_admfam,list_comfam=list_comfam,list_fat=list_fat,list_mot=list_mot)
        
@app.route("/recommendations", methods=['GET'])
def get_recommendations():
    graduatekey = request.args.get('graduatekey', default=None, type=str)
    num_reco = request.args.get("number", default=5, type=int)
    distance = request.args.get("distance", default="cosine", type=str)
    field = request.args.get("field", default="graduatekey", type=str)
    if not graduatekey:
        return jsonify("Missing Corresponding background"), 400
    elif distance not in ["cosine", "euclidean"]:
        return jsonify("Distance can only be cosine or euclidean"), 400
    elif num_reco not in range(1, 21):
        return jsonify("Can only request between 1 and 21 backgrounds"), 400
    elif graduatekey not in graduatekey_list:
        return jsonify("This graduatekey is not in supported backgrounds"), 400
    elif field not in graduate_data[0].keys():
        return jsonify("Field not available in the data"), 400
    else:
        try:
            selected_background = next(item for item in graduate_data if item['graduatekey'] == graduatekey)
            similar_backgrounds = [graduate_data[i][field] for i in selected_background[distance]]
            return jsonify(similar_backgrounds[:num_reco]), 200
        except Exception as e:
            return jsonify(str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)