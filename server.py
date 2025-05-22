from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from app import getliveTemp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='mcp_server.log')
logger = logging.getLogger('mcp_server')

# Initialize MCP server
mcp = FastMCP("weather-api-mcp")

@mcp.tool()
async def getLiveTemperature(latitude: float, longitude: float):
    """
    Get live temperature for a specific location.

    Args:
        latitude: The latitude coordinate (e.g., 40.7128 for New York)
        longitude: The longitude coordinate (e.g., -74.0060 for New York)

    Returns:
        A dictionary containing temperature information or an error message
    """
    logger.info(f"Received request for coordinates: {latitude}, {longitude}")
    result = getliveTemp(latitude, longitude)
    logger.info(f"Result: {result}")
    return result


if __name__ == "_main_":
    logger.info("Starting MCP server...")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error running MCP server: {str(e)}")
        raise