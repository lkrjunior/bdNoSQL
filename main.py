import configparser

config = configparser.RawConfigParser()
config.read('config.properties')
connectionString = config.get('DatabaseSection', 'database.connectionstring')

print(connectionString)
