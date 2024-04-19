from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from schemas import task_schema
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
api = Api(app, title='MVP Gerenciador de Tarefas', doc='/doc/', default='APIs do MVP')

CORS(app)

task_model = api.model('Task', task_schema)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)



@api.route('/tasks')
class TaskList(Resource):
    @api.expect(task_model, validate=True)
    @api.doc(responses={201: 'Created', 400: 'Bad Request'})
    
    def post(self):
        """Criar uma nova tarefa"""
        data = request.json
        new_task = Task(title=data['title'], description=data['description'])
        db.session.add(new_task)
        db.session.commit()
        return {'message': 'Task created successfully'}, 201

     
    
    def get(self):
        """Buscar todas as tarefas cadastradas"""
        tasks = Task.query.all()
        task_list = []
        for task in tasks:
            task_list.append({'id': task.id, 'title': task.title, 'description': task.description})
        return jsonify(task_list)

class TaskResource(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    
    def delete(self, id):
        """Excluir uma tarefa através do Id"""
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully'}, 200

api.add_resource(TaskResource, '/tasks/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


