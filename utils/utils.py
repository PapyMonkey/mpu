import os

class	Utils():
	def	_is_valid_id(self, id):
		return True if (id.isnumeric() and len(id) == 18) else False

	def	_db_pathfile(self, guild):
		return (os.getcwd() + '/rsc/db_' + str(guild.id) + '.json')

	def	x_to_dico(self, data):
		return ({data: ''})

utils = Utils()