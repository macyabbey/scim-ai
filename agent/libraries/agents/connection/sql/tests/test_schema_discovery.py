import os

from dotenv import load_dotenv
from scimaiagentsconnectionsql.sql_agent import agent

load_dotenv()


def test_detect_user_schemas_in_ecommerce() -> None:
    connection_string = '"' + os.environ["ECOMMERCE_POSTGRES_CONNECTION_STRING"] + '"'

    answer = agent.run(
        "Using the connection string " + connection_string + " read the database schema. \n"
        "For each of the following entity types, (user, group), "
        "determine what tables can store the entity data. An entity may be stored in mutiple tables. " # based on the example entities. \n"
        "\n\nReturn a dictionary with the entity type as the key and a list of relevant TableDescription objects "
        "as a value. "
    )
    
    print(answer)
    
    assert "user" in answer

