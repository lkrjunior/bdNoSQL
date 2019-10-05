import configparser

config = configparser.RawConfigParser()
config.read('config.properties')
connectionString = config.get('DatabaseSection', 'database.connectionString')

print(connectionString)
