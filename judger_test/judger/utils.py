import pprint

pp = pprint.PrettyPrinter(indent=4)
def dump(*args, **kwargs):
	pp.pprint(*args, **kwargs)

# .split()
# ' '.join()