from flask_restx import fields

task_schema = {
    'title': fields.String(required=True, description='Tarefas Domésticas'),
    'description': fields.String(required=True, description='Lavar a louça suja')
}
