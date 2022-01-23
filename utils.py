import os

def get_filesize_mb(path):
	return os.path.getsize(path)/1000/1000