# Azure Database for PostgreSQL MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) Server that let’s your AI applications and models talk to data hosted in Azure Database for PostgreSQL according to the MCP standard!

This server exposes the following capabilities, which can be invoked or requested by MCP Clients in your AI agents, AI applications or tools like Claude Desktop or Visual Studio Code:

- **Tools**: 
    - **query_data**: Execute read queries to retrieve data from your Azure Database for PostgreSQL databases.
    - **update_values**: Insert or update records in your database.
    - **create_table**: Create a new table in your database.
    - **drop_table**: Delete a table in your database.
- **Resources**:
    - **Tables**: Provides schema information and metadata for each table in the database, including table names and owners, column names and data types, storage parameters, and more.

By integrating with this MCP server, you can effortlessly build AI agents and applications that can intelligently and efficiently manage, analyze and make decisions based on your business data in Azure Database for PostgreSQL.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) 3.10 or above
- An Azure Database for PostgreSQL flexible server instance with a database containing your business data. For instructions on creating a flexible instance, setting up a database, and connecting to it, please refer to this [quickstart guide](https://learn.microsoft.com/azure/postgresql/flexible-server/quickstart-create-server).
- An MCP Client application or tool such as [Claude Desktop](https://claude.ai/download) or [Visual Studio Code](https://code.visualstudio.com/download).

### Installation

1. Clone the `azure-postgresql-mcp` repository:

    ```
    git clone https://github.com/Azure-Samples/azure-postgresql-mcp.git
    cd azure-postgresql-mcp
    ```

    Alternatively, you can download only the `azure_postgresql_mcp.py` file to your working folder.

2.	Create a virtual environment:

    ```
    python -m venv azure-postgresql-mcp-venv
    \azure-postgresql-mcp-venv\Scripts\activate
    ```

3. Install the dependencies:

    ```
    pip install mcp[cli]
    pip install psycopg[binary]
    ```


### Option 1: Use the MCP Server with Claude Desktop

To use the Azure Database for PostgreSQL MCP server with the Claude Desktop app, follow these instructions:
1. In the Claude Desktop app, navigate to the “Settings” pane, select the “Developer” tab and click on “Edit Config”.
2. Open the `claude_desktop_config.json` file and add the following configuration to the "mcpServers" section to configure the Azure Database for PostgreSQL MCP server:

    ```json
    {
        "mcpServers": {
            "azure-postgresql-mcp”: {
                “command”: “<path to the virtual environment>\\azure-postgresql-mcp-venv\\Scripts\\python",
                "args": [
                    "<path to azure_postgresql_mcp.py file>\\ azure_postgresql_mcp.py"
                ],
                "env": {
                    "PGHOST": "<Fully qualified name of your Azure Database for PostgreSQL instance>",
                    "PGUSER": "<Your Azure Database for PostgreSQL username>",
                    "PGPASSWORD": "<Your password>",
                    "PGDATABASE": "<Your database name>"
                }
            }        
        }
    }
    ```
3. Restart the Claude Desktop app.
4. Upon restarting, you should see a hammer icon and an attach icon at the bottom of the input box. Selecting these icons will display the tools and resources provided by the MCP Server.

You are now all set to start interacting with your data using natural language queries!

### Option 2: Use the MCP Server with Visual Studio Code

To use this MCP Server with Visual Studio Code, follow these instructions:
1. In Visual Studio Code, navigate to “File”, select “Preferences” and then choose “Settings”.
2. Search for “MCP” and select “Edit in settings.json”.
3. Add the following configuration to the “mcp” section of the `settings.json` file:

    ```JSON
    {
        "mcp": {
            "inputs": [],
            "servers": {
                "azure-postgresql-mcp": {
                    "command": “<path to the virtual environment>\\azure-postgresql-mcp-venv\\Scripts\\python",
                    "args": [
                        "<path to azure_postgresql_mcp.py file>\\ azure_postgresql_mcp.py"
                    ],
                    "env": {
                    "PGHOST": "<Fully qualified name of your Azure Database for PostgreSQL instance>",
                    "PGUSER": "<Your Azure Database for PostgreSQL username>",
                    "PGPASSWORD": "<Your password>",
                    "PGDATABASE": "<Your database name>"
                    }
                }
            }
        }
    }
    ```
4. Select the “Copilot” status icon in the upper-right corner to open the GitHub Copilot Chat window. 
5. Choose “Agent mode” from the dropdown at the bottom of the chat input box.
5. Click on “Select Tools” (hammer icon) to view the Tools exposed by the MCP Server.

You are now all set to start interacting with your data using natural language queries!

## Contributing
Contributions are welcome! For more details, see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License
This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE.md) file.
