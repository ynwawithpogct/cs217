from app import app, tree
from flask import render_template, redirect, url_for, request, jsonify
from app.forms import violationForm, nextForm, backForm, clearQuerry, homeForm, searchForm, queryForm

list_search = []
list_search_temp = []
list_query = []


@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = searchForm()
    form2 = queryForm()
    if form1.validate_on_submit() and form1.search.data:
        return redirect(url_for('search'))
    if form2.validate_on_submit() and form2.query.data:
        global list_query, list_search, list_search_temp
        # list_query = []
        list_search = tree.search_laws()
        list_search_temp = [item for item in list_search if item not in list_query]
        return redirect(url_for('create_query'))
    return render_template('index.html', searchForm=form1, queryForm=form2)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # print('reload')
    form1 = violationForm()
    form2 = nextForm()
    form3 = homeForm()

    global list_search, list_search_temp
    
    if form1.validate_on_submit() and form1.submit.data:
        loivipham = None if form1.loivipham.data is None or form1.loivipham.data == "" else form1.loivipham.data
        phuongTien = None if form1.phuongTien.data is None or form1.phuongTien.data == "" else form1.phuongTien.data
        chiTietLoi = None if form1.chiTietLoi.data is None or form1.chiTietLoi.data == "" else form1.chiTietLoi.data
        temp_list_search = tree.search_laws(loivipham, phuongTien, chiTietLoi)
        if len(temp_list_search) == 0:
            # print("Submit không thành công")
            return render_template('search.html', form=form1, nextForm=form2, listIsEmty=True)
        list_search = temp_list_search
        list_search_temp = [item for item in list_search if item not in list_query]
        return redirect(url_for('search_list'))
    if form2.validate_on_submit() and form2.next.data:
        if len(list_search) == 0:
            # print("Next không thành công")
            return render_template('search.html', form=form1, nextForm=form2, homeForm=form3, listIsEmty=True)
        return redirect(url_for('search_list'))
    if form3.validate_on_submit() and form3.home.data:
        return redirect(url_for('index'))
    return render_template('search.html', form=form1, nextForm=form2, homeForm=form3, listIsEmty=False)


@app.route('/search_list', methods=['GET', 'POST'])
def search_list():
    if len(list_search) == 0:
        return redirect(url_for('search'))
    form1 = backForm()
    form2 = nextForm()
    if form1.validate_on_submit() and form1.back.data:
        return redirect(url_for('search'))
    if form2.validate_on_submit() and form2.next.data:
        return redirect(url_for('create_query'))
    return render_template('search_list.html', backForm=form1, nextForm=form2, list_search=list_search_temp)

@app.route('/add_query/<index>')
def add_query(index):
    global list_query, list_search_temp
    index = int(index)
    if index > 0 or index < len(list_search_temp):
        item = list_search_temp[index]
        if item in list_query:
            return redirect(url_for('create_query'))
        list_search_temp.remove(item)
        list_query.append(item)
        return redirect(url_for('create_query'))
    return redirect(url_for('create_query'))

@app.route('/remove_query/<index>')
def remove_query(index):
    global list_query, list_search, list_search_temp
    index = int(index)
    if index > 0 or index < len(list_query):
        item = list_query[index]
        if item not in list_search:
            # return jsonify({"status": "error", "message": "Item in a different List Search"})
            list_query.remove(item)
            return redirect(url_for('create_query'))
        list_query.remove(item)
        list_search_temp.append(item)
        return redirect(url_for('create_query'))
    if item in list_search_temp:
        return redirect(url_for('create_query'))
    return redirect(url_for('create_query'))

@app.route('/clear_query')
def clear_query():
    global list_query, list_search, list_search_temp
    for item in list_query:
        if item in list_search and item not in list_search_temp:
            list_search_temp.append(item)
    list_query = []
    return redirect(url_for('create_query'))

@app.route('/create_query', methods=['GET', 'POST'])
def create_query():
    global list_query, list_search, list_search_temp
    form1 = backForm()
    form2 = nextForm()
    form3 = clearQuerry()
    if form1.validate_on_submit() and form1.back.data:
        return redirect(url_for('search_list'))
    if form2.validate_on_submit() and form2.next.data:
        return redirect(url_for('calculate_penalty'))
    if form3.validate_on_submit() and form3.clear.data:
        return redirect(url_for('clear_query'))
    return render_template('create_query.html', backForm=form1, nextForm=form2, clearQuerry=form3, list_search=list_search, list_search_temp=list_search_temp, list_query=list_query)


@app.route('/calculate_penalty', methods=['GET', 'POST'])
def calculate_penalty():
    global list_query
    if len(list_query) == 0:
        return redirect(url_for('create_query'))
    penalty = tree.calculate_total_penalty_with_details(list_query)
    form1 = backForm()
    form2 = homeForm()
    if form1.validate_on_submit() and form1.back.data:
        return redirect(url_for('create_query'))
    if form2.validate_on_submit() and form2.home.data:
        return redirect(url_for('index'))
    totalMinPenalty = penalty["total_min_penalty"]
    totalMaxPenalty = penalty["total_max_penalty"]
    canCuLuat = [ccl for ccl in penalty["canCuLuat"] if ccl != "" and ccl is not None]
    phatBoSung = [pbs for pbs in penalty["phatBoSung"] if pbs != "" and pbs is not None]
    return render_template('calculate_penalty.html', backForm=form1, homeForm=form2, list_query=list_query, totalMinPenalty = totalMinPenalty, totalMaxPenalty = totalMaxPenalty, canCuLuat = canCuLuat, phatBoSung = phatBoSung)
