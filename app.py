
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Medbuk9403#'
app.config['MYSQL_DB'] = 'flask_crud'
mysql = MySQL(app)


# Settings
app.secret_key = 'mysecretkey'


# Se crea la ruta "principal" donde se podran ver renderizados todos los cursos que existen en la BD
@app.route('/')
def show_all():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courses')
    data = cur.fetchall()
    return render_template('index.html', courses = data)


# Se crea una ruta parcial donde  se crean los curzos y al final redirije la ruta a la vista principal.
@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        course = [request.form['name'], request.form['teacher'], request.form['level']]
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO courses (name, teacher, level) VALUES (%s, %s, %s)',
            (course[0], course[1], course[2]))
        mysql.connection.commit()
        flash('Course Added succesfully')
        return redirect(url_for('show_all'))
        

# Se crea una ruta al hipervinculo donde por medio del ID lo busca en la BD y renderiza el curso editado con sus atributos de la BD para ser editados.
@app.route('/edit/<id>')
def get_course(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM courses WHERE id = {id}')
    data = cur.fetchall()
    return render_template('edit-course.html', course = data[0])


# Se crea una ruta parcial la cual actualiza los datos editados del curse y al final redirije la ruta a la vista principal. 
@app.route('/update/<id>', methods = ['POST'])
def update_course(id):
    if request.method == 'POST': 
        course = [request.form['name'], request.form['teacher'], request.form['level']]
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE courses
            SET name = %s, 
                teacher = %s, 
                level = %s 
            WHERE id = %s
            """, (course[0], course[1], course[2], id))
        mysql.connection.commit()

        flash('Course Updated Succesfully')
        return redirect(url_for('show_all'))


#Se crea una que redirije al hipervinculo la cual coje el id del course para ser buscado en la BD y posteriomrnete ser eliminado con una sentencia DELETE.
@app.route('/delete/<string:id>')
def delete_course(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM courses WHERE id = {id}')
    mysql.connection.commit()
    flash('Course deleted succesfully')
    return redirect(url_for('show_all'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)