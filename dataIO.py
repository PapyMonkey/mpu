import json

class DataIO():
	def	_read_json(self, filename):
		with open(filename, encoding='utf-8', mode="r") as f:
			data = json.load(f)
		return data

	def	_save_json(self, filename, data):
		with open(filename, encoding='utf-8', mode="w") as f:
			json.dump(data, f, indent=4 ,sort_keys=True, separators=(',',' : '))
		return data

	def	is_valid_json(self, filename):
		try:
			self._read_json(filename)
			return True
		except FileNotFoundError:
			return False
		except json.decoder.JSONDecodeError:
			return False

dataIO = DataIO()