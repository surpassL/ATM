import pickle

info = {
    'name': 'admin',
    'password': 'admin',
    'power': 'admin',
    'state': 0,
    'quota': 0,
    'balance': 0,
}

with open('admin.pkl', 'wb') as f:
    pickle.dump(info, f)
