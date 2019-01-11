from flask import current_app as app
from flask import Blueprint, render_template, g
from flask_assets import Bundle, Environment
import json
from . import r
from . import db
from . import preview

headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

main_blueprint = Blueprint('main', __name__, template_folder='templates', static_folder='static', root_path='application')

assets = Environment(app)
js = Bundle('js/bin/*.js', filters='jsmin', output='dist/packed.js')
scss = Bundle('scss/*.scss', filters='libsass', output='dist/all.css')
assets.register('scss_all', scss)
assets.register('js_all', js)



@main_blueprint.route('/', methods=['GET', 'POST'])
def entry():
    # base_url = redis_store.get('ENDPOINT')
    uri = r.get('uri')
    query = r.get('query')
    query_like = r.get('query_like')
    print('uri', uri)
    print('query', query)
    database = db.LynxData(uri, query, query_like)
    posts = database.records
    for post in posts:
        preview_html = preview.make_preview(post)
        print('postpreview = ', preview_html)
    return render_template('layout.html', results=posts)
