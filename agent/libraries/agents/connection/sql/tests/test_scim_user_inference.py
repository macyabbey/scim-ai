import os

from dotenv import load_dotenv
from scimaiagentsconnectionsql.sql_agent import agent
from scimaicommon.scimexampleobjects import full_enterprise_user

load_dotenv()

def test_scim_capbilities_from_minimal_schema() -> None:
    
    user_tables = [
        {
            "table_name": "users",
            "schema_name": "public",
            "fully_qualified_name": "public.users",
            "columns": [
                {
                    "name": "id",
                    "type": "INTEGER",
                    "nullable": False,
                    "default": None,
                    "check": None,
                    "check_name": None,
                },
                {
                    "name": "username",
                    "type": "VARCHAR",
                    "nullable": False,
                    "default": None,
                    "check": None,
                    "check_name": None,
                },
                {
                    "name": "email",
                    "type": "VARCHAR",
                    "nullable": False,
                    "default": None,
                    "check": None,
                    "check_name": None,
                },
                {
                    "name": "password",
                    "type": "VARCHAR",
                    "nullable": False,
                    "default": None,
                    "check": None,
                    "check_name": None,
                },
            ],
            "foreign_keys": [],
            "primary_key": {"constrained_columns": ["id"]},
        }
    ]
    
    answer = agent.run(
        "For each attribute of the Full Enterprise User Example, determine if the user related database schema can store it. \n"
        "For the attributes which can contain multiple attributes, (emails, addresses, phoneNumbers, ims, photos, groups), determine if the schema can store zero, 1 or many values. \n"
        "For the attributes which contain objects, (name, urn:ietf:params:scim:schemas:extension:enterprise:2.0:User, meta), evaluate each sub-attribute. \n\n"
        "User Related Database Schema: " + str(user_tables) + "\n\n"
        "Full Enterprise User Example: " + str(full_enterprise_user) + "\n\n" 
        "Return a dictionary with the attribute name as the key and a dictionary as the value. The dictionary value should contain a key of schema, table, column, and support. The value for the support key should be one of the following: 'zero', 'one', 'many', 'not supported'." 
    )
    
    print(str(answer))
    
        # assert "User" or 'users' in java_classes
        # assert "Profiles" or 'profies' in java_classes
