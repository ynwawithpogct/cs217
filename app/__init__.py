from flask import Flask
import json
from flask_wtf.csrf import CSRFProtect
from app.models import ViolationTree
# from app.utils import print_tree


app = Flask(__name__)
app.config.from_object('config.Config')
csrf = CSRFProtect()
csrf.init_app(app)

with open('app/loi.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
tree = ViolationTree()
tree.build_tree_from_json(data)
# print_tree(tree.root)
from app import routes