import yaml

with open('config.yaml', 'r') as config:

    docs = yaml.load_all(config)
    for doc in docs:
        mode = doc['mode']
        print mode
        '''for k, v in doc.items():
            print doc[k]
            print k, "->", v'''