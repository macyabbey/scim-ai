import subprocess
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from smolagents import tool
import yaml

script_path = Path(__file__).parent
server_cwd = script_path / ".." / ".." / ".." / ".." / ".." / ".." / ".." / ".." / "server"
server_abs_cwd = server_cwd.resolve()
generated_jpa_class_directory = server_abs_cwd / "target" / "generated-sources" / "jpa" / "com" / "scim" / "ai" / "server" / "persistence" / "entities"
generated_jpa_package = "com.scim.ai.server.persistence.entities"

class GenerateResult(BaseModel):
    """Represents the result of an attempt to generate JPA classes.

    Attributes:
        model_config (ConfigDict): Configuration for the model, set to strict mode.
        success (bool): Indicates whether the server start attempt was successful.
        error_message (str | None): Contains the error message if the server start attempt failed, otherwise None.
        message (str | None): Contains the message from the server start attempt
        exit_code (int): The exit code of the server start attempt.
        jpa_classes (list[str]): List of JPA classes generated and available in EntityManager
    """

    model_config = ConfigDict(strict=True)
    success: bool
    error_message: str | None
    message: str | None
    exit_code: int
    jpa_classes: list[str] | None

class AddSqlConnectionResult(BaseModel):
    """Represents the result of adding sql connection configuration.

    Attributes:
        model_config (ConfigDict): Configuration for the model, set to strict mode.
        success (bool): Indicates whether adding the sql connection succeeded
        error_message (str | None): Contains the error message if adding the sql connection failed
        message (str | None): Contains the message
        jpa_classes (list[str]): List of JPA classes generated and available in EntityManager
    """

    model_config = ConfigDict(strict=True)
    success: bool
    error_message: str | None
    message: str | None
    jpa_classes: list[str] | None

def parse_database_type(database_connection_string: str) -> str:
  """Parses the database type from a database connection string.

  Args:
    database_connection_string: Connection string to the sql database

  Returns:
    The database type extracted from the connection string, or 'unknown' if not found.
  """
  if database_connection_string.startswith("postgresql://"):
    return "postgresql"
  elif database_connection_string.startswith("mysql://"):
    return "mysql"
  else:
    return "unknown"

def parse_database_username(database_connection_string: str) -> str:
  """Parses the username from a database connection string.

  Args:
    database_connection_string: Connection string to the sql database

  Returns:
    The username extracted from the connection string, or 'unknown' if not found.
  """
  try:
    return database_connection_string.split("//")[1].split(":")[0]
  except IndexError:
    return "unknown"
    
def parse_database_password(database_connection_string: str) -> str:
  """Parses the password from a database connection string.

  Args:
      database_connection_string: Connection string to the sql database

  Returns:
      The password extracted from the connection string, or 'unknown' if not found.
  """
  try:
      return database_connection_string.split("//")[1].split(":")[1].split("@")[0]
  except IndexError:
      return "unknown"

default_datasource_name = "db"
default_template_values = {
  # root pom.xml
  # Postgres driver / version for hibernate tools
  #
  # <groupId>org.postgresql</groupId>
  # <artifactId>postgresql</artifactId>
  # <version>${version.lib.postgresql}</version>
  #
  # helidon modules
  # <dependency>
  #     <groupId>io.helidon.integrations.db</groupId>
  #     <artifactId>helidon-integrations-db-pgsql</artifactId>
  # </dependency>
  # <dependency>
  #     <groupId>io.helidon.integrations.db</groupId>
  #     <artifactId>helidon-integrations-db-mysql</artifactId>
  # </dependency>
  "root_pom_xml": {
    "helidon-integrations-db": "helidon-integrations-db-pgsql",
    "driver-group": "<groupId>org.postgresql</groupId>",
    "driver-artifact": "<artifactId>postgresql</artifactId>",
    "driver-version": "<version>${version.lib.postgresql}</version>",
  },
  # Update hibernate.properties    
  # hibernate.connection.driver_class=org.postgresql.Driver
  # hibernate.connection.url=jdbc:postgresql://localhost:5432/ecommerce_db
  # hibernate.connection.username=postgres
  # hibernate.connection.password=postgres
  "hibernate_properties": {
    "driver-class": "org.postgresql.Driver",
    "jdbc-url": "jdbc:postgresql://localhost:5432/ecommerce_db",
    "connection-username": "hibernate.connection.username=postgres",
    "connection-password": "hibernate.connection.password=postgres"
  },
  # Update resource/META-INF/persistence.xml
  #     <?xml version="1.0" encoding="UTF-8"?>
  # <persistence xmlns="https://jakarta.ee/xml/ns/persistence"
  #              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  #              xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence
  #                                  https://jakarta.ee/xml/ns/persistence/persistence_3_1.xsd"
  #              version="3.1">
  #     <persistence-unit name="db" transaction-type="JTA">
  #         <jta-data-source>db</jta-data-source>
  #         <class>com.scim.ai.server.persistence.User</class>
  #         <properties>
  #             <property name="hibernate.column_ordering_strategy" value="legacy"/>
  #             <!-- https://docs.jboss.org/hibernate/orm/6.3/dialect/dialect.html -->
  #             <property name="hibernate.dialect" value="org.hibernate.dialect.PostgreSQLDialect"/>
  #         </properties>
  #     </persistence-unit>
  # </persistence>
  "persistence_xml": {
    "data-source-name": f"name=\"{default_datasource_name}\"",
    "data-source-node": f"<jta-data-source>{default_datasource_name}</jta-data-source>",
    "hibernate-dialect": "org.hibernate.dialect.PostgreSQLDialect",
    "jpa-classes": "<class>com.scim.ai.server.persistence.User</class>",
  },
  # see README.md for details how to run databases in docker
  # javax:
  #   sql:
  #     DataSource:
  #       db:
  #         datasource:
  #           url: "postgresql://localhost:5432/ecommerce_db"
  #           username: "postgres"
  #           password: "postgres"
  #           initializationFailTimeout: -1
  #           connectionTimeout: 2000
  #           helidon:
  #             pool-metrics:
  #               enabled: true
  #               # name prefix defaults to "db.pool." - if you have more than one client within a JVM, you may want to distinguish between them
  #               name-prefix: "hikari."
  #         services:
  #           tracing:
  #             - enabled: true
  #           metrics:
  #             - type: TIMER
  #         health-check:
  #           type: "query"
  #           statementName: "health-check"
  "application_yaml": {
    "datasource": {
      "url": "postgresql://localhost:5432/ecommerce_db",
      "username": "postgres",
      "password": "postgres",
      "initializationFailTimeout": -1,
      "connectionTimeout": 2000,
      "helidon": {
        "pool-metrics": {
          "enabled": True,
          "name-prefix": "hikari."
        }
      }
    },
    "services": {
      "tracing": {
        "enabled": True
      },
      "metrics": {
        "type": "TIMER"
      }
    },
    "health-check": {
      "type": "query",
      "statementName": "health-check"
    }
  }
}

def get_database_type_values(
    database_type: str, 
    datasource_name: str,
    jdbc_url: str,
) -> dict[str, dict[str, str]]:

    if database_type == "postgresql":
        return {
            "root_pom_xml": {
              "helidon-integrations-db": "helidon-integrations-db-pgsql",
              "driver-group": "<groupId>org.postgresql<groupId>",
              "driver-artifact": "<artifactId>postgresql</artifactId>",
              "driver-version": "<version>${version.lib.postgresql}</version>",
            },
            "hibernate_properties": {
              "driver-class": "org.postgresql.Driver",
              "jdbc-url": jdbc_url,
            },
            "persistence_xml": {
              "data-source-name": f"name=\"{datasource_name}\"",
              "data-source-node": f"<jta-data-source>{datasource_name}</jta-data-source>",
              "hibernate-dialect": "org.hibernate.dialect.PostgreSQLDialect",
            },
            "application_yaml": {
              "datasource": {
                "url": "postgresql://localhost:5432/ecommerce_db",
                "username": "postgres",
                "password": "postgres",
                "initializationFailTimeout": -1,
                "connectionTimeout": 2000,
                "helidon": {
                  "pool-metrics": {
                    "enabled": True,
                    "name-prefix": "hikari."
                  }
                }
              },
              "services": {
                "tracing": {
                  "enabled": True
                },
                "metrics": {
                  "type": "TIMER"
                }
              },
              "health-check": {
                "type": "query",
                "statementName": "health-check"
              }
            }
        }
    elif database_type == "mysql":
        return {
            "root_pom_xml": {
              "helidon-integrations-db": "helidon-integrations-db-pgsql",
              "driver-group": "<groupId>org.postgresql<groupId>",
              "driver-artifact": "<artifactId>postgresql</artifactId>",
              "driver-version": "<version>${version.lib.postgresql}</version>",
            },
            "hibernate_properties": {
              "driver-class": "org.postgresql.Driver",
              "jdbc-url": jdbc_url,
            },
            "persistence_xml": {
              "data-source-name": f"name=\"{datasource_name}\"",
              "data-source-node": f"<jta-data-source>{datasource_name}</jta-data-source>",
              "hibernate-dialect": "org.hibernate.dialect.PostgreSQLDialect",
            },
            "application_yaml": {
              "datasource": {
                "url": "mysql://localhost:5432/mysql",
                "username": "mysql",
                "password": "mysql",
                "initializationFailTimeout": -1,
                "connectionTimeout": 2000,
                "helidon": {
                  "pool-metrics": {
                    "enabled": True,
                    "name-prefix": "hikari."
                  }
                }
              },
              "services": {
                "tracing": {
                  "enabled": True
                },
                "metrics": {
                  "type": "TIMER"
                }
              },
              "health-check": {
                "type": "query",
                "statementName": "health-check"
              }
            }
        }
    else:
        return {}
    
def generate_jpa_models(
    generated_jpa_class_directory: str,
    generated_jpa_package: str
) -> GenerateResult:
    # Generate JPA models from database schema
    # Return a list of JPA classes
    result = subprocess.run(
        ["bash", "generate.sh"],
        cwd=server_abs_cwd,
        capture_output=True,
        text=True, check=False,
    )

    exit_code = result.returncode
    stdout = result.stdout
    stderr = result.stderr
    jpa_classes = []
    
    if exit_code == 0:
      # Read generated JPA classes from generated_jpa_class_directory
      for jpa_class_file in generated_jpa_class_directory.glob("*.java"):
        jpa_class_name = jpa_class_file.stem
        jpa_classes.append(f"{generated_jpa_package}.{jpa_class_name}")

    return GenerateResult(
        success=exit_code == 0,
        error_message=stderr if stderr else None,
        message=stdout if stdout else None,
        exit_code=exit_code,
        jpa_classes=jpa_classes
    )

def replace_values_in_file(
        file_path: Path, 
        template_values: dict[str, str],
        database_type_values: dict[str, str]) -> None:
    with open(file_path, "r") as file:
      persistence_xml_content = file.read()
        
    for key, value in template_values.items():
      persistence_xml_content = persistence_xml_content.replace(value, database_type_values.get(key, value))
    
    with open(file_path, "w") as file:
      file.write(persistence_xml_content)
      
    return None

def update_persistence_xml(
    path: Path,
    template_values: dict[str],
    database_type_values: dict[str],
 ) -> None:
    replace_values_in_file(
        path, 
        template_values,
        database_type_values
    )
    return None
    
def update_hibernate_properties(
    path: Path,
    template_values: dict[str],
    database_type_values: dict[str],
) -> None:
    replace_values_in_file(
        path, 
        template_values,
        database_type_values
    )
    return None


def update_root_pom_xml(
    path: Path,
    template_values: dict[str],
    database_type_values: dict[str],
) -> None:
    replace_values_in_file(
        path, 
        template_values,
        database_type_values
    )
    return None

def update_application_yaml(
    path: Path,
    datasource_name: str,
    database_type_values: dict[str],
) -> None:
    
    # Read in the application_xml file
    with open(path, "r") as file:
        application_yaml_content = file.read()
        
    # Parse application_yaml_content as yaml
    application_yaml_data = yaml.safe_load(application_yaml_content)
    
    # Remove javax.sql.DataSource key with the same name as variable default_datasource_name from application_yaml_content
    if "javax" in application_yaml_data and "sql" in application_yaml_data["javax"] and "DataSource" in application_yaml_data["javax"]["sql"]:
      application_yaml_data["javax"]["sql"]["DataSource"].pop(default_datasource_name, None)
      
    # Add javax.sql.DataSource[datasource_name] = database_type_values
    if "javax" not in application_yaml_data:
      application_yaml_data["javax"] = {}
    if "sql" not in application_yaml_data["javax"]:
      application_yaml_data["javax"]["sql"] = {}
    if "DataSource" not in application_yaml_data["javax"]["sql"]:
      application_yaml_data["javax"]["sql"]["DataSource"] = {}
    
    application_yaml_data["javax"]["sql"]["DataSource"][datasource_name] = database_type_values
    
    # Write the serialized application_yaml_content with two space indents back to the file
    with open(path, "w") as file:
      yaml.dump(application_yaml_data, file, default_flow_style=False, indent=2)
    return None


@tool
def add_sql_connection(datasource_name: str, database_connection_string: str) -> AddSqlConnectionResult:
    """Updates various configuration in the java server so it will be able to connect with the sql database.

    May fail if the connection string is for a type of sql database that is not yet supported.

    Args:
        datasource_name: Datasource name for use in EntityManager and application.yaml
        database_connection_string: Connection string to the sql database

    Returns a AddSqlConnectionResult.
    
    """
    database_type = parse_database_type(database_connection_string)
    database_username = parse_database_username(database_connection_string)
    database_password = parse_database_password(database_connection_string)

    if database_type == "unknown":
        return AddSqlConnectionResult(
            success=False, 
            error_message="Database type not supported", 
            message=None,
            jpa_classes=None
        )
    
    database_type_values = get_database_type_values(
        database_type, 
        datasource_name,
        database_connection_string
    )
    
    update_root_pom_xml(
        server_abs_cwd / "pom.xml",
        default_template_values["root_pom_xml"],
        database_type_values["root_pom_xml"]
     )

    hibernate_properties_values = {
      **database_type_values["hibernate_properties"],
      "connection-username": f"hibernate.connection.username={database_username}",
      "connection-password": f"hibernate.connection.password={database_password}"
    }

    update_hibernate_properties(
      server_abs_cwd / "src" / "main" / "resources" / "hibernate.properties",
      default_template_values["hibernate_properties"],
      hibernate_properties_values
    )
    
    generate_result = generate_jpa_models(
        generated_jpa_class_directory,
        generated_jpa_package
    )
    
    if not generate_result.success:
        return AddSqlConnectionResult(
            success=False, 
            error_message=generate_result.error_message, 
            message=generate_result.message,
            jpa_classes=None
        )
    
    # Create a new dictionary with updated credentials instead of mutating the original
    updated_application_yaml = {
      **database_type_values["application_yaml"],
      "datasource": {
        **database_type_values["application_yaml"]["datasource"],
        "username": database_username,
        "password": database_password
      }
    }
    
    # Update application.yaml with the new immutable dictionary
    update_application_yaml(
      server_abs_cwd / "src" / "main" / "resources" / "application.yaml",
      datasource_name,
      updated_application_yaml
    )
    
    jpa_class_nodes = "\n        ".join(f"<class>{jpa_class}</class>" for jpa_class in generate_result.jpa_classes)
    
    # Create a new dictionary with updated persistence_xml values
    updated_persistence_xml = {
      **database_type_values["persistence_xml"],
      "jpa-classes": jpa_class_nodes
    }
    
    # Update persistence.xml with the new immutable dictionary
    update_persistence_xml(
      server_abs_cwd / "src" / "main" / "resources" / "META-INF" / "persistence.xml",
      default_template_values["persistence_xml"],
      updated_persistence_xml
    )
    
    return AddSqlConnectionResult(
        success=True, 
        error_message=None, 
        message="Successfully added sql connection",
        jpa_classes=generate_result.jpa_classes
    )