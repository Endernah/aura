from flask import Flask, request, jsonify, render_template, redirect
import json, bcrypt

app = Flask('Aura')

class Auth:
    global hash_password, check_password

    def hash_password(user, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def create_user(username, password, name):
        with open('users.json', 'r') as file:
            users = json.load(file)
        new_user = {
            'name': name,
            'password': hash_password(username, password),
            'pfp': 'default.png',
            'auras': 50,
            'auras_given': {}
        }
        users[username] = new_user
        with open('auras.json', 'w') as file:
            json.dump(users, file)
        
        return new_user

    def check_password(user, user_password):
        hashed_password = user.get('password')
        return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_auras():
    try:
        if file:
            file = None
    except:
        pass
    with open('auras.json', 'r') as file:
        return json.load(file)

def get_profile(profile_name):
    auras = get_auras()
    profile_name = profile_name.replace(" ", "_").lower()
    try:
        profile = auras.get(profile_name)
        if profile is None:
            return False
    except:
        return False
    return profile

def search_profile(query):
    auras = get_auras()
    results = []
    for profile_name in auras.keys():
        if query.lower() in profile_name.lower():
            results.append(profile_name)
    return results

def search_profile_v2(query):
    auras = get_auras()
    results = [aura.get('name') for aura in auras.values() if query in aura.get('name').lower()]
    return jsonify(results)

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('q')
    if len(query.lower()[:2]) < 2 or not all(char.isalpha() for char in query.lower()[:2]):
        return jsonify({'error': 'Invalid query'})
    return search_profile_v2(query.lower())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    try:
        query = request.args.get('s')
        if query is None:
            return redirect('/')
    except:
        return redirect('/')
    if len(query.lower()[:2]) < 2 or not all(char.isalpha() for char in query.lower()[:2]):
        return redirect('/')
    r = search_profile(str(query).replace(" ", "_").lower())
    results = []
    search_results = "Search results:"
    for result in r:
        results.append(get_profile(result).get('name'))
    if len(results) == 0:
        search_results = "No results found for " + query
    def work(result):
        return str(result).replace(" ", "_").lower()
    return render_template('search.html', results=results, search_results=search_results, work=work)

@app.route('/profile')
def profile():
    try:
        profile = request.args.get('p')
        if profile is None:
            return redirect('/')
    except:
        return redirect('/')
    pulled_profile = get_profile(profile)
    if pulled_profile is False:
        return render_template('not_found.html')
    name = pulled_profile.get('name')
    auras = pulled_profile.get('auras')
    auras_given = pulled_profile.get('auras_given')
    pfp = f"/static/pfp/{pulled_profile.get('pfp')}"
    return render_template('profile.html', name=name, auras=auras, auras_given=auras_given, pfp=pfp)

app.run(host='0.0.0.0', port=80, debug=True)