from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes/new')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/dasboard')

    return render_template('new_recipe.html')

@app.route('/recipes/new/process', methods=['POST'])
def process_recipe():
    if 'user_id' not in session:
        return redirect('/dasboard')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'made_on': request.form['made_on']
    }
    Recipe.save(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    return render_template('view_recipe.html',recipe=Recipe.get_by_id({'id': id}),user=User.get_by_id(data))

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    return render_template('edit_recipe.html',recipe=Recipe.get_by_id({'id': id}),user=User.get_by_id(data))


@app.route('/recipes/edit/process/<int:id>', methods=['POST'])
def process_edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'made_on': request.form['made_on']
    }

    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')

    Recipe.delete({'id':id})
    return redirect('/dashboard')