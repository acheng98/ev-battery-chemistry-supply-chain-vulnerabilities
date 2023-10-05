import glob, os

if __name__ == '__main__':
	for dirpath, dirnames, filenames in os.walk("."):
		for filename in [f for f in filenames if f.endswith(".txt")]:
			path = os.path.join(dirpath, filename)
			
			with open(path, 'r') as file:
				data = file.read()
				data = data.replace("Türkiye", "Turkey")

			with open(path, 'w') as file:
				file.write(data)