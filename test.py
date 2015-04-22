import yaml
config = open('config.yaml', 'r')
docs = yaml.load_all(config)
for doc in docs:
    parameters = doc.copy()

for i in parameters:
    print i+': '+parameters[i]