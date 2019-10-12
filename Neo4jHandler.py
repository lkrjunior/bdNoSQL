from neo4j import GraphDatabase

from INeo4jHandler import INeo4jHandler


class Neo4jHandler(INeo4jHandler):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def createMessage(self, message):
        with self._driver.session() as session:
            messageWrite = session.write_transaction(self._create_and_return_message, message)
            print(messageWrite)

    @staticmethod
    def _create_and_return_message(tx, message):
        result = tx.run("CREATE (a:Test) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def createTwitterAnalysis(self, location, sentimental):
        with self._driver.session() as session:
            messageWrite = session.write_transaction(self._create_and_return_twitter_analysis, location, sentimental)
            print(messageWrite)

    @staticmethod
    def _create_and_return_twitter_analysis(tx, location, sentimental):
        result = tx.run("CREATE (a:" + location + ") "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=sentimental)
        return result.single()[0]

    @staticmethod
    def _execute_command(tx, command):
        tx.run(command)

    @staticmethod
    def _execute_command_return_first(tx, command):
        result = tx.run(command)
        return result.single()[0]

    @staticmethod
    def _execute_command_return_list(tx, command):
        result = tx.run(command)
        return result.single()

    def clean(self):
        command = "MATCH (n)"\
                  "DETACH DELETE n"
        with self._driver.session() as session:
            session.write_transaction(self._execute_command, command)

    def insertSentimentals(self, listSentimentals):
        for item in listSentimentals:
            key = item
            value = listSentimentals[key]
            command = "CREATE (" + key + ":Sentimental {title:'" + key + "'})"
            with self._driver.session() as session:
                session.write_transaction(self._execute_command, command)

    #def insertTweets(self, listTweets):
        #for item in listTweets:
            #neo4j.createTwitterAnalysis(item['sentimental'], item['location'])

    #def insertRelations(self):


    def close(self):
        self._driver.close()

'''
Scripts for example

CREATE (RS:Estado {title:'Rio Grande do Sul', estado:'Rio Grande do Sul'})
CREATE (PortoAlegre:Cidade {title:'Porto Alegre', estado:'Rio Grande do Sul'})
CREATE (Negativo:Sentimento {title:'Negativo'})
CREATE (Positivo:Sentimento {title:'Positivo'})
CREATE (Neutro:Sentimento {title:'Neutro'})
CREATE
  (Negativo)-[:POSSUI {percentual:['35%']}]->(PortoAlegre),
  (Positivo)-[:POSSUI {percentual:['25%']}]->(PortoAlegre),
  (Neutro)-[:POSSUI {percentual:['40%']}]->(PortoAlegre)
  
CREATE (Alvorada:Cidade {title:'Alvorada', estado:'Rio Grande do Sul'})
CREATE
  (Negativo)-[:POSSUI {percentual:['35%']}]->(Alvorada),
  (Positivo)-[:POSSUI {percentual:['35%']}]->(Alvorada),
  (Neutro)-[:POSSUI {percentual:['30%']}]->(Alvorada)

CREATE
  (PortoAlegre)-[:ESTA {tipo:['capital']}]->(RS),
  (Alvorada)-[:ESTA {tipo:['cidade']}]->(RS)
'''