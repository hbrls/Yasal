## 来源：docker-gordon-ai_20250629.md

When you have installed MCP servers, you can add clients to the MCP Toolkit. These clients can interact with the installed MCP servers, turning the MCP Toolkit into a gateway.To install a client:

1. In Docker Desktop, select MCP Toolkit and select the Clients tab.
2. Find the client of your choice and select Connect.Your client can now interact with the MCP Toolkit.

### Example: Use Claude Desktop as a client (#example-use-claude-desktop-as-a-client)

Imagine you have Claude Desktop installed, and you want to use the GitHub MCP server, and the Puppeteer MCP server, you do not have to install the servers in Claude Desktop. You can simply install these 2 MCP servers in the MCP Toolkit, and add Claude Desktop as a client:

1. From the MCP Toolkit menu, select the Catalog tab and find the Puppeteer server and add it.
2. Repeat for the GitHub server.
3. From the Clients tab, select Connect next to Claude Desktop. Restart Claude Desktop if it's running, and it can now access all the servers in the MCP Toolkit.
4. Within Claude Desktop, run a test by submitting the following prompt using the Sonnet 3.5 model:

Take a screenshot of docs.docker.com and then invert the colors

Make sure to allow Gordon to interact with GitHub by selecting Always allow in Gordon's answer.