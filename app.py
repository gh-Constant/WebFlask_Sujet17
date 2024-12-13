from flask import Flask, request, render_template, redirect, url_for, abort, flash, g

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="constantsuchet",
            password="Password123!",
            database="monuments_db",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db



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