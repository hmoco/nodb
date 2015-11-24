import pytest

from nodb import *

@pytest.fixture
def populate_data():
	return {
		'people': [
			{'name': 'Chance',
			'profession': 'musician',
			'age': 22},
			{'name': 'Donnie Trumpet',
			'profession': 'musician',
			'age': False}
		],
		'songs': [
			{'title': 'Miracle',
			'by': 'Donnie Trumpet'},
			{'title': 'Home Studio', 
			'by': 'Chance'},
		]
	}

def test_filter(populate_data):
	db = Nodb()
	db.load(populate_data)
	miracles = db['songs'].filter(lambda x: x['title'] == 'Miracle')
	assert len(list(miracles)) == 1

def test_find_one(populate_data):
	db = Nodb()
	db.load(populate_data)
	assert db['people'].find_one({'name':'Chance'})

def test_update(populate_data):
	db = Nodb()
	db.load(populate_data)
	db['people'].update({'profession':'rapper'}, {'name':'Chance'})
	assert db['people'].find_one({'name':'Chance'})['profession'] == 'rapper'

def test_chain(populate_data):
	db = Nodb()
	db.load(populate_data)
	db['people'].filter(lambda x: x['age'] == 22).update({'profession':'rapper'})
	assert db['people'].find_one({'name':'Chance'})['profession'] == 'rapper'

def test_Q(populate_data):
	db = Nodb()
	db.load(populate_data)
	chance = db['people'].filter(
			Q('name', 'eq', 'Chance')
		)
	assert len(list(chance)) == 1
	assert list(chance)[0]['name'] == 'Chance'


def test_Q_and(populate_data):
	db = Nodb()
	db.load(populate_data)
	chance = db['people'].find(
			Q('profession', 'eq', 'musician') & Q('age', 'eq', 22)
		)
	assert len(list(chance)) == 1
	assert list(chance)[0]['name'] == 'Chance'

def test_Q_and(populate_data):
	db = Nodb()
	db.load(populate_data)
	sox = db['people'].find(
			Q('name', 'eq', 'Donnie Trumpet') | Q('name', 'eq', 'Chance')
		)
	assert len(list(sox)) == 2
