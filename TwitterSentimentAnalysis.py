import configparser
from Neo4jHandler import Neo4jHandler
from TwitterHandler import TwitterHandler
from MongoDbConnection import MongoDbConnection
from ComprehendHandler import ComprehendHandler

config = configparser.RawConfigParser()
config.read('config.properties')

section = 'DatabaseSection'
connectionString = config.get(section, 'database.connectionString')

section = 'TwitterSection'
consumerKey = config.get(section, 'twitter.consumerKey')
consumerSecret = config.get(section, 'twitter.consumerSecret')
accessToken = config.get(section, 'twitter.accessToken')
accessTokenSecret = config.get(section, 'twitter.accessTokenSecret')

section = 'Neo4jSection'
connectionStringNeo4j = config.get(section, 'neo4j.connectionString')
userNeo4j = config.get(section, 'neo4j.user')
passwordNeo4j = config.get(section, 'neo4j.password')

section = 'ComprehendSection'
accessKeyComprehend = config.get(section, 'comprehend.accessKey')
secretAccessKeyComprehend = config.get(section, 'comprehend.secretAccessKey')

mongoDbConnection = MongoDbConnection(connectionString)
twitter = TwitterHandler(consumerKey, consumerSecret, accessToken, accessTokenSecret)
neo4j = Neo4jHandler(connectionStringNeo4j, userNeo4j, passwordNeo4j)
comprehendHandler = ComprehendHandler(accessKeyComprehend, secretAccessKeyComprehend)



mongoDbConnection.close()
twitter.close()
neo4j.close()
comprehendHandler.close()
