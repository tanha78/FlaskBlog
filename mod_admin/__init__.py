from flask import Blueprint


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def amin_index():
    return 'Hello from admin index'