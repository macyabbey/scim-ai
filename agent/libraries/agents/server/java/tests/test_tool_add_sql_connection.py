import pytest
import os
import tempfile
import yaml
from unittest.mock import patch, MagicMock
from pathlib import Path

from dotenv import load_dotenv
from scimaiagentsserverjava.tools.add_sql_connection import (
  add_sql_connection,
  update_application_yaml,
  update_root_pom_xml,
  update_hibernate_properties,
  update_persistence_xml,
  generate_jpa_models,
  default_template_values
)

load_dotenv()
    
 # Get real content from the provided files
REAL_APPLICATION_YAML = """# filepath: scim-ai/server/src/main/resources/application.yaml
# see README.md for details how to run databases in docker
javax:
  sql:
    DataSource:
      db:
        datasource:
          url: "postgresql://localhost:5432/ecommerce_db"
          username: "postgres"
          password: "postgres"
          initializationFailTimeout: -1
          connectionTimeout: 2000
          helidon:
            pool-metrics:
              enabled: true
              # name prefix defaults to "db.pool." - if you have more than one client within a JVM, you may want to distinguish between them
              name-prefix: "hikari."
        services:
          tracing:
            - enabled: true
          metrics:
            - type: TIMER
        health-check:
          type: "query"
          statementName: "health-check"
"""

REAL_POM_XML = """<!-- filepath: scim-ai/server/pom.xml -->
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>io.helidon.applications</groupId>
        <artifactId>helidon-mp</artifactId>
        <version>4.1.6</version>
        <relativePath/>
    </parent>
    <groupId>com.scim.ai.server</groupId>
    <artifactId>scim-ai-server</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <name>Scim AI Server</name>

    <dependencies>
        <!-- REMOVED SOME ACTUAL pom.xml content for testing -->
        <!-- Start: https://helidon.io/docs/v4/mp/persistence -->
        <!-- Start: https://helidon.io/docs/v4/mp/persistence#DS -->
        <dependency>
            <groupId>io.helidon.integrations.db</groupId>
            <artifactId>helidon-integrations-db-pgsql</artifactId>
        </dependency>
        <dependency>
            <groupId>io.helidon.integrations.db</groupId>
            <artifactId>helidon-integrations-db-mysql</artifactId>
        </dependency>
        <dependency>
            <groupId>io.helidon.integrations.cdi</groupId>
            <artifactId>helidon-integrations-cdi-datasource-hikaricp</artifactId>
            <scope>runtime</scope>
        </dependency>
        <!-- End: https://helidon.io/docs/v4/mp/persistence#DS -->
        <!-- Start: https://helidon.io/docs/v4/mp/persistence#JTA -->
        <dependency>
            <groupId>jakarta.transaction</groupId>
            <artifactId>jakarta.transaction-api</artifactId>
            <version>2.0.1</version>
            <scope>compile</scope> 
        </dependency>
        <dependency>
            <groupId>io.helidon.integrations.cdi</groupId>
            <artifactId>helidon-integrations-cdi-jta-weld</artifactId>
            <scope>runtime</scope> 
        </dependency>
        <!-- End: https://helidon.io/docs/v4/mp/persistence#JTA -->
        <!-- Start: https://helidon.io/docs/v4/mp/persistence#JPA -->
        <dependency>
            <groupId>jakarta.persistence</groupId>
            <artifactId>jakarta.persistence-api</artifactId>
            <version>3.1.0</version>
            <scope>compile</scope> 
        </dependency>
        <dependency>
            <groupId>io.helidon.integrations.cdi</groupId>
            <artifactId>helidon-integrations-cdi-jpa</artifactId>
            <scope>runtime</scope> 
        </dependency>
        <dependency>
            <groupId>io.helidon.integrations.cdi</groupId>
            <artifactId>helidon-integrations-cdi-hibernate</artifactId>
            <scope>runtime</scope> 
        </dependency>
        <!-- End: https://helidon.io/docs/v4/mp/persistence#JPA -->
        <!-- End: https://helidon.io/docs/v4/mp/persistence -->
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-dependency-plugin</artifactId>
                <executions>
                    <execution>
                        <id>copy-libs</id>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>io.smallrye</groupId>
                <artifactId>jandex-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <id>make-index</id>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.hibernate.tool</groupId>
                <artifactId>hibernate-tools-maven</artifactId>
                <version>${version.lib.hibernate}</version>
                <dependencies>
                    <dependency>
                        <groupId>org.hibernate.tool</groupId>
                        <artifactId>hibernate-tools-orm</artifactId>
                        <version>${version.lib.hibernate}</version>
                    </dependency>
                    <dependency>
                        <!-- 
                           See where parent helidon pom already declares the postgres version 
                           https://github.com/helidon-io/helidon/blob/95af89efb622b90fe578cd2443c835ef2aa7afad/dependencies/pom.xml#L828C26-L828C40
                        -->
                        <groupId>org.postgresql</groupId>
                        <artifactId>postgresql</artifactId>
                        <version>${version.lib.postgresql}</version>
                    </dependency>
                </dependencies>
                <executions>
                    <execution>
                        <?m2e execute onConfiguration?>
                        <id>entity-generation</id>
                        <phase>generate-sources</phase>
                        <goals>
                            <goal>hbm2java</goal>
                        </goals>
                        <configuration>
                            <ejb3>true</ejb3>
                            <jdk5>true</jdk5>
                            <packageName>com.scim.ai.server.persistence.entities</packageName>
                            <outputDirectory>${project.build.directory}/generated-sources/jpa</outputDirectory>
                        </configuration>
                    </execution>
                </executions>
            </plugin>      
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <executions>
                    <execution>
                        <?m2e execute onConfiguration?>
                        <id>default-compile</id>
                        <configuration>
                            <annotationProcessorPaths>
                                <annotationProcessorPath>
                                    <groupId>org.hibernate.orm</groupId>
                                    <artifactId>hibernate-jpamodelgen</artifactId> 
                                    <version>${version.lib.hibernate}</version> 
                                </annotationProcessorPath>
                            </annotationProcessorPaths>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <!-- Start: https://helidon.io/docs/v4/mp/persistence#JPA-MetaModel -->
        
            <plugin>
                <groupId>org.hibernate.orm.tooling</groupId>
                <artifactId>hibernate-enhance-maven-plugin</artifactId>
                <!--
                    Ideally, your plugin versions are managed via a
                    <pluginManagement> element, which is why the <version> element
                    is commented out below.  If, nevertheless, you opt for the
                    explicit version, check
                    https://search.maven.org/artifact/org.hibernate.orm/hibernate-enhance-maven-plugin
                    for up-to-date versions, and make sure the version is the same
                    as that of Hibernate ORM itself.
                -->
                <!-- <version>6.3.1.Final</version> -->
                <executions>
                    <execution>
                        <?m2e execute onConfiguration?>
                        <id>Statically enhance JPA entities for Hibernate</id>
                        <phase>compile</phase>
                        <goals>
                            <goal>enhance</goal>
                        </goals>
                        <configuration>
                            <failOnError>true</failOnError>
                            <enableDirtyTracking>true</enableDirtyTracking>
                            <enableLazyInitialization>true</enableLazyInitialization>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <!-- End: https://helidon.io/docs/v4/mp/persistence#JPA-MetaModel -->
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>build-helper-maven-plugin</artifactId>
                <version>3.6.0</version>
                <executions>
                    <execution>
                        <?m2e execute onConfiguration?>
                        <phase>generate-sources</phase>
                        <goals>
                            <goal>add-source</goal>
                        </goals>
                        <configuration>
                            <sources>
                                <source>${project.build.directory}/generated-sources/jpa</source>
                            </sources>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
"""

REAL_HIBERNATE_PROPERTIES = """hibernate.connection.driver_class=org.postgresql.Driver
hibernate.connection.url=jdbc:postgresql://localhost:5432/ecommerce_db
hibernate.connection.username=postgres
hibernate.connection.password=postgres
"""

REAL_PERSISTENCE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence
                                 https://jakarta.ee/xml/ns/persistence/persistence_3_1.xsd"
             version="3.1">
    <persistence-unit name="db" transaction-type="JTA">
        <jta-data-source>db</jta-data-source>
        <class>com.scim.ai.server.persistence.User</class>
        <properties>
            <property name="hibernate.column_ordering_strategy" value="legacy"/>
            <!-- https://docs.jboss.org/hibernate/orm/6.3/dialect/dialect.html -->
            <property name="hibernate.dialect" value="org.hibernate.dialect.PostgreSQLDialect"/>
        </properties>
    </persistence-unit>
</persistence>
"""

@pytest.fixture
def temp_files():
    """Create temporary files with real content for testing."""
    temp_dir = tempfile.TemporaryDirectory()
    
    # Create temporary files with real content
    app_yaml_path = os.path.join(temp_dir.name, "application.yaml")
    with open(app_yaml_path, "w") as f:
        f.write(REAL_APPLICATION_YAML)
        
    pom_xml_path = os.path.join(temp_dir.name, "pom.xml")
    with open(pom_xml_path, "w") as f:
        f.write(REAL_POM_XML)
        
    hibernate_properties_path = os.path.join(temp_dir.name, "hibernate.properties")
    with open(hibernate_properties_path, "w") as f:
        f.write(REAL_HIBERNATE_PROPERTIES)
        
    persistence_xml_path = os.path.join(temp_dir.name, "persistence.xml")
    with open(persistence_xml_path, "w") as f:
        f.write(REAL_PERSISTENCE_XML)
    
    yield {
        "temp_dir": temp_dir,
        "app_yaml_path": app_yaml_path,
        "pom_xml_path": pom_xml_path,
        "hibernate_properties_path": hibernate_properties_path,
        "persistence_xml_path": persistence_xml_path
    }
    
    temp_dir.cleanup()

def test_update_application_yaml(temp_files):
    """Test updating application.yaml with database configuration."""
    test_data_source = "testSource"
    
    db_config = {
        "datasource": {
          "url": "jdbc:mysql://localhost:3306/testdb",
          "username": "testuser",
          "password": "testpass",
          "driver": "com.mysql.cj.jdbc.Driver"
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
    
    result = update_application_yaml(
        temp_files["app_yaml_path"],
        "testSource",
        db_config
    )

    assert result is None
    
    # Read the updated file
    with open(temp_files["app_yaml_path"], "r") as f:
        updated_content = f.read()
    
    updated_yaml_contents = yaml.safe_load(updated_content)
    
    
    # Verify the content was updated correctly
    assert "db" not in updated_yaml_contents["javax"]["sql"]["DataSource"]
    assert test_data_source in updated_yaml_contents["javax"]["sql"]["DataSource"]
    
    datasource_config = updated_yaml_contents["javax"]["sql"]["DataSource"][test_data_source]["datasource"]
    
    assert datasource_config["url"] == db_config["datasource"]["url"]
    assert datasource_config["username"] == db_config["datasource"]["username"]
    assert datasource_config["password"] == db_config["datasource"]["password"]


def test_update_root_pom_xml(temp_files):
    """Test updating root pom.xml with database dependencies."""
    
    root_pom_values = {
      "helidon-integrations-db": "helidon-integrations-db-mysql",
      "driver-group": "<groupId>org.mysql<groupId>",
      "driver-artifact": "<artifactId>mysql</artifactId>",
      "driver-version": "<version>${version.lib.mysql}</version>",
    }
    
    result = update_root_pom_xml(
        temp_files["pom_xml_path"],
        default_template_values["root_pom_xml"],
        root_pom_values
    )
    assert result is None
    
    # Read the updated file
    with open(temp_files["pom_xml_path"], "r") as f:
        updated_content = f.read()
    
    # Verify the content was updated correctly
    assert "helidon-integrations-db-mysql" in updated_content
    assert "<groupId>org.mysql<groupId>" in updated_content
    assert "<artifactId>mysql</artifactId>" in updated_content
    assert "<version>${version.lib.mysql}</version>" in updated_content

@patch('scimaiagentsserverjava.tools.add_sql_connection.subprocess.run')
def test_generate_jpa_models_success(mock_run):
    """Test successfully generating JPA models from database schema."""
    # Mock successful subprocess execution
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "JPA classes generated successfully"
    mock_process.stderr = ""
    mock_run.return_value = mock_process
    
    # Mock finding generated Java files
    mock_jpa_dir = MagicMock(spec=Path)
    mock_java_file1 = MagicMock(spec=Path)
    mock_java_file1.stem = "User"
    mock_java_file2 = MagicMock(spec=Path)
    mock_java_file2.stem = "Product"
    mock_jpa_dir.glob.return_value = [mock_java_file1, mock_java_file2]
    
    # Call the function
    result = generate_jpa_models(mock_jpa_dir, "com.test.package")
    
    # Verify
    assert result.success is True
    assert result.error_message is None
    assert result.message == "JPA classes generated successfully"
    assert result.exit_code == 0
    assert result.jpa_classes == ["com.test.package.User", "com.test.package.Product"]
    mock_run.assert_called_once()

@patch('scimaiagentsserverjava.tools.add_sql_connection.subprocess.run')
def test_generate_jpa_models_failure(mock_run):
    """Test failure when generating JPA models from database schema."""
    # Mock failed subprocess execution
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stdout = ""
    mock_process.stderr = "Failed to connect to database"
    mock_run.return_value = mock_process
    
    # Mock finding generated Java files (should be empty since generation failed)
    mock_jpa_dir = MagicMock(spec=Path)
    mock_jpa_dir.glob.return_value = []
    
    # Call the function
    result = generate_jpa_models(mock_jpa_dir, "com.test.package")
    
    # Verify
    assert result.success is False
    assert result.error_message == "Failed to connect to database"
    assert result.message is None
    assert result.exit_code == 1
    assert result.jpa_classes == []
    mock_run.assert_called_once()

def test_update_hibernate_properties(temp_files):
    """Test updating hibernate.properties with database configuration."""
    db_config = {
      "driver-class": "org.mysql.Driver",
      "jdbc-url": "jdbc:foo:foo//localhost:5432/ecommerce_db",
      "connection-username": "hibernate.connection.username=mysql",
      "connection-password": "hibernate.connection.password=mysql"
    }
    
    result = update_hibernate_properties(
        temp_files["hibernate_properties_path"],
        default_template_values["hibernate_properties"],
        db_config
    )
    assert result is None
    
    # Read the updated file
    with open(temp_files["hibernate_properties_path"], "r") as f:
        updated_content = f.read()
    
    # Verify the content was updated correctly
    assert "org.mysql.Driver" in updated_content
    assert "jdbc:foo:foo//localhost:5432/ecommerce_db" in updated_content
    assert "hibernate.connection.password=mysql" in updated_content
    assert "hibernate.connection.username=mysql" in updated_content
    

def test_update_persistence_xml(temp_files):
    """Test updating persistence.xml with database configuration."""
    
    test_data_source = "testSource"
    
    db_config = {
        "data-source-name": f"name=\"{test_data_source}\"",
        "data-source-node": f"<jta-data-source>{test_data_source}</jta-data-source>",
        "jpa-classes": "<class>com.scim.ai.server.persistence.Cat</class>\n        <class>com.scim.ai.server.persistence.Dog</class>"
    }
    
    result = update_persistence_xml(
        temp_files["persistence_xml_path"], 
        default_template_values["persistence_xml"],
        db_config
    )
    assert result is None
    
    # Read the updated file
    with open(temp_files["persistence_xml_path"], "r") as f:
        updated_content = f.read()
    
    # Verify the content was updated correctly
    assert f"name=\"{test_data_source}\"" in updated_content
    assert f"<jta-data-source>{test_data_source}</jta-data-source>" in updated_content
    assert db_config["jpa-classes"] in updated_content
