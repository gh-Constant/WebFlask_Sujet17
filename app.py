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
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_epoque")
    typesEpoque = mycursor.fetchall()
    mycursor.execute("SELECT * FROM tableaux ORDER BY RAND() LIMIT 3")
    featured_monuments = mycursor.fetchall()
    return render_template('accueil.html', typesEpoque=typesEpoque, featured_monuments=featured_monuments)

if __name__ == '__main__':
    app.run()

@app.route('/type-epoque/show')
def show_type_epoque():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_epoque")
    typesEpoque = mycursor.fetchall()
    return render_template('type_epoque/show_type_epoque.html', typesEpoque=typesEpoque)

@app.route('/type-epoque/add', methods=['GET'])
def add_type_epoque():
    return render_template('type_epoque/add_type_epoque.html')

@app.route('/type-epoque/add', methods=['POST'])
def valid_add_type_epoque():
    libelle = request.form.get('libelle', '')
    mycursor = get_db().cursor()
    sql = "INSERT INTO type_epoque (libelle) VALUES (%s)"
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/type-epoque/show')

@app.route('/type-epoque/delete', methods=['GET'])
def delete_type_epoque():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    
    # Get all tableaux using this type_epoque
    sql = "SELECT * FROM tableaux WHERE typeEpoque_id = %s"
    mycursor.execute(sql, (id,))
    related_tableaux = mycursor.fetchall()
    
    # Get the type_epoque details
    sql = "SELECT * FROM type_epoque WHERE id = %s"
    mycursor.execute(sql, (id,))
    type_epoque = mycursor.fetchone()
    
    if not related_tableaux:
        # If no related tableaux, delete directly
        sql = "DELETE FROM type_epoque WHERE id = %s"
        mycursor.execute(sql, (id,))
        get_db().commit()
        flash(u'Type époque supprimé, id: ' + str(id), 'alert-warning')
        return redirect('/type-epoque/show')
    
    # If there are related tableaux, show confirmation page
    return render_template('type_epoque/confirm_delete.html', 
                         type_epoque=type_epoque, 
                         related_tableaux=related_tableaux)

@app.route('/type-epoque/delete', methods=['POST'])
def delete_type_epoque_confirm():
    id = request.form.get('id')
    mycursor = get_db().cursor()
    
    # Delete related tableaux first
    sql = "DELETE FROM tableaux WHERE typeEpoque_id = %s"
    mycursor.execute(sql, (id,))
    
    # Then delete the type_epoque
    sql = "DELETE FROM type_epoque WHERE id = %s"
    mycursor.execute(sql, (id,))
    get_db().commit()
    
    flash(u'Type époque et tableaux associés supprimés', 'alert-warning')
    return redirect('/type-epoque/show')

@app.route('/type-epoque/edit', methods=['GET'])
def edit_type_epoque():
    id = request.args.get('id', '')
    id=int(id)
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_epoque")
    type_epoque = mycursor.fetchall()
    type_epoque = type_epoque[id-1] 
    return render_template('type_epoque/edit_type_epoque.html', type_epoque=type_epoque)

@app.route('/type-epoque/edit', methods=['POST'])
def valid_edit_type_epoque():
    libelle = request.form['libelle']
    id = request.form.get('id', '')
    mycursor = get_db().cursor()
    sql = "UPDATE type_epoque SET libelle = %s WHERE id = %s"
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    message=u'type tableau modifié, id: ' + id + " libelle : " + libelle
    flash(message, 'alert-success')
    return redirect('/type-epoque/show')

@app.route('/tableau/show')
def show_tableau():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM tableaux")
    tableaux = mycursor.fetchall()
    mycursor.execute("SELECT * FROM type_epoque")

    typesEpoque = mycursor.fetchall()

    return render_template('tableau/show_tableau.html', tableaux=tableaux, typesEpoque=typesEpoque)

@app.route('/tableau/add', methods=['GET'])
def add_tableau():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_epoque")
    type_epoque = mycursor.fetchall()   
    return render_template('tableau/add_tableau.html', typesEpoque=type_epoque)

@app.route('/tableau/add', methods=['POST'])
def valid_add_tableau():
    nomTableau = request.form.get('nomTableau', '')
    prixAssurance = request.form.get('prixAssurance', '')
    dateRealisation = request.form.get('dateRealisation', '')
    peintre = request.form.get('peintre', '')
    localisationMusee = request.form.get('localisationMusee', '')
    typeEpoque_id = request.form.get('typeEpoque_id', '')
    photo = request.form.get('photo', '')
    mouvement = request.form.get('mouvement', '')

    mycursor = get_db().cursor()
    sql = "INSERT INTO tableaux (nomTableau, prixAssurance, dateRealisation, peintre, localisationMusee, photo, mouvement, typeEpoque_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (nomTableau, prixAssurance, dateRealisation, peintre, localisationMusee, photo, mouvement, typeEpoque_id))
    get_db().commit()

    message = u'tableau ajouté , nom:'+nomTableau + '---- type_epoque_id :' + typeEpoque_id + ' ---- prixAssurance:' + prixAssurance + ' - dateRealisation:'+  dateRealisation + ' - peintre:' + peintre + ' - localisationMusee:' + localisationMusee + ' - photo:' + photo + ' - mouvement:' + mouvement
    print(message)
    flash(message, 'alert-success')
    return redirect('/tableau/show')

@app.route('/tableau/delete', methods=['GET'])
def delete_tableau():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = "DELETE FROM tableaux WHERE id = " + str(id)
    mycursor.execute(sql)
    get_db().commit()
    message=u'un tableau supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/tableau/show')

@app.route('/tableau/edit', methods=['GET'])
def edit_tableau():
    id = request.args.get('id', '')
    id = int(id)
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM tableaux WHERE id = %s", (id,))
    tableau = mycursor.fetchone()
    
    if not tableau:
        flash('Tableau not found', 'alert-d anger')
        return redirect('/tableau/show')

    mycursor.execute("SELECT * FROM type_epoque")
    typesEpoque = mycursor.fetchall()
    return render_template('tableau/edit_tableau.html', tableau=tableau, typesEpoque=typesEpoque)

@app.route('/tableau/edit', methods=['POST'])
def valid_edit_tableau():
    nomTableau = request.form.get('nomTableau', '')
    prixAssurance = request.form.get('prixAssurance', '')
    dateRealisation = request.form.get('dateRealisation', '')
    peintre = request.form.get('peintre', '')
    localisationMusee = request.form.get('localisationMusee', '')
    photo = request.form.get('photo', '')
    mouvement = request.form.get('mouvement', '')
    typeEpoque_id = request.form.get('typeEpoque_id', '')
    id = request.form.get('id', '')

    mycursor = get_db().cursor()
    sql = """UPDATE tableaux SET nomTableau = %s, prixAssurance = %s, dateRealisation = %s,
                 peintre = %s, localisationMusee = %s, photo = %s,
                 mouvement = %s, typeEpoque_id = %s 
             WHERE id = %s"""
    
    mycursor.execute(sql, (nomTableau, prixAssurance, dateRealisation, 
                          peintre, localisationMusee, photo,
                          mouvement, typeEpoque_id, id))
    get_db().commit()
    
    message = u'tableau modifié, id: ' + id
    flash(message, 'alert-success')
    return redirect('/tableau/show')

@app.route('/tableau/filtre', methods=['GET'])
def filtre_tableau():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_epoque")
    typesEpoque = mycursor.fetchall()
    mycursor.execute("SELECT * FROM tableaux")
    tableaux = mycursor.fetchall() 
    return render_template('tableau/filtre_tableau.html', tableaux=tableaux, typesEpoque=typesEpoque)

@app.route('/tableau/filtre', methods=['POST'])
def valid_filtre_tableau():
    TableauNameFilter = request.form.get('TableauNameFilter', '')
    typeEpoque_id = request.form.get('typeEpoque_id', '')
    prixMin = request.form.get('prixMin', '')
    prixMax = request.form.get('prixMax', '')

    sql = "SELECT * FROM tableaux WHERE 1=1"
    params = ()  

    
    if TableauNameFilter:
        sql += " AND nomTableau LIKE %s"
        params += (f"%{TableauNameFilter}%",)
    
    if typeEpoque_id:
        sql += " AND typeEpoque_id = %s"    
        params += (typeEpoque_id,)
    
    if prixMin:
        sql += " AND prixAssurance >= %s"
        params += (prixMin,)
    
    if prixMax:
        sql += " AND prixAssurance <= %s"
        params += (prixMax,)

    mycursor = get_db().cursor()
    mycursor.execute(sql, params)  
    tableaux = mycursor.fetchall()

    mycursor.execute("SELECT * FROM type_epoque")
    typesEpoque = mycursor.fetchall()

    return render_template('tableau/filtre_tableau.html', tableaux=tableaux, typesEpoque=typesEpoque)
