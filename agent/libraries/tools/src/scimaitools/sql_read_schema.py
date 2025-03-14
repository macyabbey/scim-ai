"""Module provides functionality to read and describe the schema of a database using SQLAlchemy and Pydantic.

Classes:
    PrimaryKeyDescription: Describes the primary key of a database schema.
    ForeignKeyDescription: Describes a foreign key relationship in a database schema.
    ColumnDescription: Represents the description of a database column.
    TableDescription: Represents the description of a database table.

Functions:
    get_column_metadata(col: Column) -> ColumnDescription:
        Retrieve metadata for a given column.
        Generate metadata for a database table.
    read_schema(database_connection_string: str) -> list[TableDescription]:
        Read what schemas and tables are present in the database and return a list of TableDescription objects.
"""
from pydantic import BaseModel, ConfigDict
from smolagents import tool
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, create_engine, inspect
from sqlalchemy.dialects.postgresql import DOMAIN


class PrimaryKeyDescription(BaseModel):
    """A class used to describe the primary key of a database schema.

    Attributes
    ----------
    model_config : ConfigDict
        Configuration dictionary for the model, set to be strict.
    constrained_columns : List[str]
        A list of column names that are constrained by the primary key.

    """

    model_config = ConfigDict(strict=True)
    constrained_columns: list[str]

class ForeignKeyDescription(BaseModel):
    """A class used to describe a foreign key relationship in a database schema.

    Attributes
    ----------
    constrained_columns : list[str]
        A list of column names in the current table that are constrained by the foreign key.
    referred_table : str
        The name of the table that the foreign key refers to.
    referred_columns : list[str]
        A list of column names in the referred table that the foreign key points to.

    """

    model_config = ConfigDict(strict=True)
    constrained_columns: list[str]
    referred_table: str
    referred_columns: list[str]

class ColumnDescription(BaseModel):
    """Represents the description of a database column.

    Attributes:
        model_config (ConfigDict): Configuration for the model, set to be strict.
        name (str): The name of the column.
        type (str): The data type of the column.
        nullable (bool): Indicates if the column can be null.
        default (str | None | bool | int | float): The default value of the column.
        check (str | None): The check constraint for the column.
        check_name (str | None): The name of the check constraint.

    """

    model_config = ConfigDict(strict=True)
    name: str
    type: str
    nullable: bool
    default: str | None | bool | int | float
    check: str | None
    check_name: str | None

class TableDescription(BaseModel):
    """Represents the description of a database table.

    Attributes:
        model_config (ConfigDict): Configuration for the model, set to strict mode.
        table_name (str): The name of the table.
        schema_name (str): The name of the schema the table belongs to.
        fully_qualified_name (str): The fully qualified name of the table.
        columns (list[ColumnDescription]): A list of column descriptions for the table.
        primary_key (PrimaryKeyDescription): The primary key description of the table.
        foreign_keys (list[ForeignKeyDescription]): A list of foreign key descriptions for the table.

    """

    model_config = ConfigDict(strict=True)
    table_name: str
    schema_name: str
    fully_qualified_name: str
    columns: list[ColumnDescription]
    primary_key: PrimaryKeyDescription
    foreign_keys: list[ForeignKeyDescription]

def get_column_metadata(col: Column) -> ColumnDescription:
    """Retrieve metadata for a given column.

    Args:
        col (Column): The column for which metadata is to be retrieved.

    Returns:
        ColumnDescription: An object containing the column's metadata, including
                           name, type, nullable status, default value, check constraint,
                           and check constraint name.

    """
    if isinstance(col["type"], DOMAIN):
        return ColumnDescription(
            name=col["name"],
            type=str(col["type"].data_type),
            nullable=col["nullable"],
            default=col["default"],
            check=str(col["type"].check),
            check_name=col["type"].name,
        )

    return ColumnDescription(
        name=col["name"],
        type=str(col["type"]),
        nullable=col["nullable"],
        default=col["default"],
        check=None,
        check_name=None,
    )

def get_table_metadata(
        name: str,
        schema: str,
        columns: list[Column],
        foreign_keys: list[ForeignKey],
        primary_key: PrimaryKeyConstraint,
) -> TableDescription:
    """Generate metadata for a database table.

    Args:
        name (str): The name of the table.
        schema (str): The schema to which the table belongs.
        columns (list[Column]): A list of Column objects representing the table's columns.
        foreign_keys (list[ForeignKey]): A list of ForeignKey objects representing the table's foreign keys.
        primary_key (PrimaryKeyConstraint): A PrimaryKeyConstraint object representing the table's primary key.

    Returns:
        TableDescription: An object containing the table's metadata, including its name, schema,
                          columns, foreign keys, and primary key.

    """
    return TableDescription(
        table_name=name,
        schema_name=schema,
        fully_qualified_name=f"{schema}.{name}",
        columns=[get_column_metadata(col) for col in columns],
        foreign_keys=[
            ForeignKeyDescription(
              constrained_columns=fk["constrained_columns"],
              referred_table=fk["referred_table"],
              referred_columns=fk["referred_columns"],
            ) for fk in foreign_keys
        ],
        primary_key=PrimaryKeyDescription(constrained_columns=primary_key["constrained_columns"]),
    )

# https://docs.sqlalchemy.org/en/21/core/reflection.html

@tool
def read_schema(database_connection_string: str) -> list[str]:
    """Read what schemas and tables are present in the database.

    Returns a json array of serialized TableDescription objects representing the tables in the database.

    Args:
        database_connection_string: A database connection string to read the schema from.

    """
    engine = create_engine(database_connection_string)
    inspector = inspect(engine)
    output = []
    for schema in inspector.get_schema_names():
        for table in inspector.get_table_names(schema):
            output.extend([
                get_table_metadata(
                    name=table,
                    schema=schema,
                    columns=inspector.get_columns(table, schema),
                    foreign_keys=inspector.get_foreign_keys(table, schema),
                    primary_key=inspector.get_pk_constraint(table, schema),
                ).model_dump_json(),
            ])
    return output
