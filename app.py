from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

typesEpoque = [
{'id': 1,'libelle': 'Renaissance'},
 {'id': 2,'libelle': 'Temps Modernes'},
 {'id': 3,'libelle': 'Contemporain'},
 {'id': 4,'libelle': 'Moyen-Age'}
]

tableaux = [
{'id':1,'nomTableau':'La Joconde', 'prixAssurance':'4000','dateRealisation':'1506-10-21', 'peintre':'Léonard de Vinci', 'localisationMusee':'Louvre', 'photo':'laJoconde.jpeg', 'mouvement':None, 'typeEpoque_id':1},
 {'id':2,'nomTableau':'Le Radeau de La Méduse', 'prixAssurance':'300.2','dateRealisation':'1819-03-15', 'peintre':'Théodore Géricault', 'localisationMusee':'Louvre', 'photo':'leRadeauDeLaMeduse.jpeg', 'mouvement':'romantisme', 'typeEpoque_id':3},
 {'id':3,'nomTableau':'Guernica', 'prixAssurance':'200.6','dateRealisation':'1937-06-04', 'peintre':'Pablo Picasso', 'localisationMusee':'Reina Sofia', 'photo':'guernica.jpeg', 'mouvement':'cubisme','typeEpoque_id':3},
 {'id':4,'nomTableau':"L'Ecole d'Athène", 'prixAssurance':'105.3','dateRealisation':'1512-02-21', 'peintre':'Raphaël', 'localisationMusee':'Vatican', 'photo':'lEcoleDAthene.jpeg', 'mouvement':'maniérisme', 'typeEpoque_id':1},
 {'id':5,'nomTableau':'La Jeune Fille à la perle', 'prixAssurance':'2040','dateRealisation':'1665-11-12', 'peintre':'Johannes Vermeer', 'localisationMusee':'Mauritshuis', 'photo':'laJeuneFilleALaPerle.jpeg', 'mouvement':'baroque', 'typeEpoque_id':2},
 {'id':6,'nomTableau':'La Laitière', 'prixAssurance':'3040','dateRealisation':'1658-05-30', 'peintre':'Johannes Vermeer', 'localisationMusee':'Rijksmuseum', 'photo':'laLaitière.jpeg', 'mouvement':'baroque', 'typeEpoque_id':2},
 {'id':7,'nomTableau':'Le Calvaire', 'prixAssurance':'5060','dateRealisation':'1505-09-30', 'peintre':'Josse Lieferinxe', 'localisationMusee':'Louvre', 'photo':'leCalvaire.jpeg','mouvement':None, 'typeEpoque_id':1},
 {'id':9,'nomTableau':'Portrait du bouffon Gonella', 'prixAssurance':'1230','dateRealisation':'1445-03-18', 'peintre':'Jean Fouquet', 'localisationMusee':'Kunsthistorisches Museum', 'photo':'leProtraitduBouffonGonella.jpeg','mouvement':None, 'typeEpoque_id':4},
 {'id':10,'nomTableau':'La liberté guidant le peuple', 'prixAssurance':'150.5','dateRealisation':'1830-12-25', 'peintre':'Eugène DelaCroix', 'localisationMusee':'Louvre', 'photo':'laLiberteGuidantlePeuple.jpeg','mouvement': 'romantisme', 'typeEpoque_id':3},
 {'id':11,'nomTableau':"Rentable de l'Agneau mystique", 'prixAssurance':'1010','dateRealisation':'1432-01-05', 'peintre':'Jan van Eyck', 'localisationMusee':'Cathédrale Saint-Bavon de Gand', 'photo':'AgneauMystique.jpeg','mouvement':None, 'typeEpoque_id':4}
]

@app.route('/')
def show_accueil():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()

@app.route('/type-epoque/show')
def show_type_epoque():
    #print(typesEpoque)
    return render_template('type_epoque/show_type_epoque.html', typesEpoque=typesEpoque)

@app.route('/type-epoque/add', methods=['GET'])
def add_type_epoque():
    return render_template('type_epoque/add_type_epoque.html')

@app.route('/type-epoque/add', methods=['POST'])
def valid_add_type_epoque():
    libelle = request.form.get('libelle', '')
    print(u'type ajouté , libellé :', libelle)
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/type-epoque/show')

@app.route('/type-epoque/delete', methods=['GET'])
def delete_type_epoque():
    id = request.args.get('id', '')
    print ("un type d'tableau supprimé, id :",id)
    message=u'un type d\'tableau supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/type-epoque/show')

@app.route('/type-epoque/edit', methods=['GET'])
def edit_type_epoque():
    id = request.args.get('id', '')
    libelle = request.args.get('libelle', '')     # comment passé plusieurs paramètres (clé primaire composés)
    id=int(id)
    type_epoque = typesEpoque[id-1]
    return render_template('type_epoque/edit_type_epoque.html', type_epoque=type_epoque)

@app.route('/type-epoque/edit', methods=['POST'])
def valid_edit_type_epoque():
    libelle = request.form['libelle']
    id = request.form.get('id', '')
    print(u'type tableau modifié, id: ',id, " libelle :", libelle)
    message=u'type tableau modifié, id: ' + id + " libelle : " + libelle
    flash(message, 'alert-success')
    return redirect('/type-epoque/show')

@app.route('/tableau/show')
def show_tableau():
    # print(tableaux)
    return render_template('tableau/show_tableau.html', tableaux=tableaux)

@app.route('/tableau/add', methods=['GET'])
def add_tableau():
    return render_template('tableau/add_tableau.html', typesEpoque=typesEpoque)

@app.route('/tableau/add', methods=['POST'])
def valid_add_tableau():
    nomTableau = request.form.get('nomTableau', '')
    prixAssurance = request.form.get('prixAssurance', '')
    dateRealisation = request.form.get('dateRealisation', '')
    peintre = request.form.get('peintre', '')
    localisationMusee = request.form.get('localisationMusee', '')
    type_epoque_id = request.form.get('type_epoque_id', '')
    photo = request.form.get('photo', '')
    mouvement = request.form.get('mouvement', '')
    message = u'tableau ajouté , nom:'+nomTableau + '---- type_epoque_id :' + type_epoque_id + ' ---- prixAssurance:' + prixAssurance + ' - dateRealisation:'+  dateRealisation + ' - peintre:' + peintre + ' - localisationMusee:' + localisationMusee + ' - photo:' + photo + ' - mouvement:' + mouvement
    print(message)
    flash(message, 'alert-success')
    return redirect('/tableau/show')

@app.route('/tableau/delete', methods=['GET'])
def delete_tableau():
    id = request.args.get('id', '')
    message=u'un tableau supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/tableau/show')

@app.route('/tableau/edit', methods=['GET'])
def edit_tableau():
    id = request.args.get('id', '')
    id=int(id)
    tableau = tableaux[id-1]
    return render_template('tableau/edit_tableau.html', tableau=tableau, typesEpoque=typesEpoque)

@app.route('/tableau/edit', methods=['POST'])
def valid_edit_tableau():
    id = request.form.get('id', '')
    nom = request.form.get('nom', '')
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    image = request.form.get('image', '')
    mouvement = request.form.get('mouvement', '')
    typesEpoque_id = request.form.get('typesEpoque_id', '')
    message = u'tableau modifié , nom:'+nom + '---- prix :' + prix + ' ---- stock:' + stock + ' ---- description:' + description + ' ---- image:' + image + ' ---- mouvement:' + mouvement + ' ---- typesEpoque_id:' + typesEpoque_id + u' ------ pour l tableau d identifiant :' + id
    print(message)
    flash(message, 'alert-success')
    return redirect('/tableau/show')

@app.route('/tableau/filtre', methods=['GET'])
def filtre_tableau():
    return render_template('tableau/filtre_tableau.html', tableau=tableaux, typesEpoque=typesEpoque)

@app.route('/tableau/filtre', methods=['POST'])
def valid_filtre_tableau():
    TableauNameFilter = request.form.get('TableauNameFilter', '')
    typeEpoque_id = request.form.get('typeEpoque_id', '')
    prixMin = request.form.get('prixMin', '')
    prixMax = request.form.get('prixMax', '')
    message = u'filtre appliqué , nom tableau:'+TableauNameFilter + '---- type_epoque_id :' + typeEpoque_id + ' ---- prixMin:' + prixMin + ' - prixMax:'+  prixMax
    flash(message, 'alert-success')
    return redirect('/tableau/filtre')