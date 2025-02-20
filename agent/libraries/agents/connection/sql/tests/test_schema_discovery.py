import os

from dotenv import load_dotenv
from scimaiagentsconnectionsql.sql_agent import agent

load_dotenv()


def test_sql_agent() -> None:
    connection_string = '"' + os.environ["ECOMMERCE_POSTGRES_CONNECTION_STRING"] + '"'

    user_and_group_tables = agent.run(
        "Using the connection string " + connection_string + " read the database schema. "
        "For each of the following entity types, (User, Group), "
        "determine what tables should store the entity data based on the example entities. \n"
        "\n\nReturn a dictionary with the entity type as the key and a list of relavent TableDescription objects "
        "as a value. ",
    )

    assert "User" in user_and_group_tables
    assert "Group" in user_and_group_tables

    java_classes = agent.run(
        "Write Spring Data JPA entity and repository classes for the the User and Group tables in the provided map.\n"
        "\nProvided map: " + str(user_and_group_tables) + ""
        "\n\nReturn a map of entity type as key and a list of strings as value. Each string should be a valid Java "
        "class.",
    )

    assert "User" in java_classes
    assert "Group" in java_classes
