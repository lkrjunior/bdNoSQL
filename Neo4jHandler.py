from neo4j import GraphDatabase

from INeo4jHandler import INeo4jHandler


class Neo4jHandler(INeo4jHandler):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def createMessage(self, message):
        with self._driver.session() as session:
            messageWrite = session.write_transaction(self._create_and_return, message)
            print(messageWrite)

    @staticmethod
    def _create_and_return(tx, message):
        result = tx.run("CREATE (a:Test) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def close(self):
        self._driver.close()

