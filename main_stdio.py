from tools import mcp  # triggers tool registration

if __name__ == "__main__":
    # Use stdio transport for Cursor MCP integration
    mcp.run(transport="stdio") 