from src.argparser import ArgParser
from src.creeper import Creeper

p = ArgParser()
args = p.parse()

c = Creeper()
c.walk(args['target'])
print(c.file_list)

for dir in args['directories']:
    c = Creeper()
    c.walk(dir)
    print(c.file_list)
