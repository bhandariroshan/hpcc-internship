import csv


class CSVWriter(object):
	"""docstring for CSVWriter"""
	def __init__(self, filename, headers, seperator, line_terminator, mode, is_writeheader=False):
		super(CSVWriter, self).__init__()
		self.filename = filename
		self.handle = open(filename + '.csv', mode, newline=line_terminator)
		self.writer = csv.DictWriter(self.handle, fieldnames=headers)
		if is_writeheader:
			self.writer.writeheader()

	def write(self, data_dict):
		self.writer.writerow(data_dict)


	def write_multiple(self, data_dict_list):
		self.writer.writerows(data_dict_list)

	def close(self):
		self.handle.close()
