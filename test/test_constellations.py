from constellations import ConstellationsWidget

const = ConstellationsWidget()

print(const.get_string())

for constellation in const.constellations: 
	if not const.check_const(str(constellation)):
		print("Failed to find " + constellation)

print(const.check_const(const.constellations))

