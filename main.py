from src.config import Config
from src.creeper import Creeper


conf = Config()
conf.parse()

c = Creeper()
c.walk(conf['target'])
print(c.file_list)

for dir in conf['directories']:
    c = Creeper()
    c.walk(dir)
    print(c.file_list)
