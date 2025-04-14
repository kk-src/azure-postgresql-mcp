"""
MCP server for Azure Database for PostgreSQL - Flexible Server

This code contains of MCP server for Azure Database for PostgreSQL - Flexible server.

Resource:
- The table schema is listed as the resource.

Tools: The following tools are exposed
- Query data
- Update values
- Create table
- Drop table.

Inorder to run in powershell the following variables should be exported are necessary:

```
$env:PGHOST="<Flex PG database instance>"
$env:PGUSER="<username>"
$env:PGPORT="<port>"
$env:PGDATABASE="<database to connect>"
$env:PGPASSWORD="<password>"
```

The mcp server can be run by:

```
python flexpg.py
```

For more details on integrations please refer to the README.

"""

import os
import sys
import urllib.parse

import psycopg

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Flex PG Explorer")


# Function to construct simple URI for resource
def get_uri():
    dbhost = os.environ["PGHOST"]
    dbname = os.environ["PGDATABASE"]
    dbhost_normalized = dbhost.split(".", 1)[0] if "." in dbhost else dbhost
    db_uri = f"flexpg://{dbhost_normalized}/{dbname}"
    return db_uri


# Function to construct URI for connection.
def get_connection_uri():
    # Read parameters from the environment
    dbhost = os.environ["PGHOST"]
    dbname = os.environ["PGDATABASE"]
    dbuser = urllib.parse.quote(os.environ["PGUSER"])
    password = os.environ["PGPASSWORD"]
    db_uri = f"host={dbhost} dbname={dbname} user={dbuser} password={password}"
    return db_uri


# MCP reseource to send back schema for all tables.
@mcp.resource(get_uri() + "/tables")
def get_schema() -> str:
    try:
        with psycopg.connect(get_connection_uri()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT table_name, column_name, data_type FROM information_schema.columns "
                    "WHERE table_schema = 'public' ORDER BY table_name, ordinal_position;"
                )
                colnames = [desc[0] for desc in cur.description]
                tables = cur.fetchall()
                ret = str(colnames) + "\n" + "\n".join(str(row) for row in tables)
    except Exception as e:
        print(f"Error: {str(e)}")
        ret = ""
    return ret


# MCP tool to query data.
@mcp.tool()
def query_data(s: str) -> str:
    try:
        with psycopg.connect(get_connection_uri()) as conn:
            with conn.cursor() as cur:
                cur.execute(s)
                rows = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                ret = str(colnames) + "\n" + ",".join(str(row) for row in rows)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        ret = ""
    return ret


# Internal function to execute and commit transaction.
def exec_and_commit(s: str) -> None:
    try:
        with psycopg.connect(get_connection_uri()) as conn:
            with conn.cursor() as cur:
                cur.execute(s)
                conn.commit()
    except Exception as e:
        print(f"Error: {str(e)}")


# MCP tool to update values in a table
@mcp.tool()
def update_values(s: str):
    exec_and_commit(s)


# MCP tool to create table in the database
@mcp.tool()
def create_table(s: str):
    exec_and_commit(s)


# MCP tool to drop table from the database
@mcp.tool()
def drop_table(s: str):
    exec_and_commit(s)


if __name__ == "__main__":
    mcp.run()