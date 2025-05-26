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


@mcp.prompt()
def weather_agent_prompt(location: str = "") -> str:
    """
    Hava durumu ajanı için bir prompt şablonu.

    Args:
        location: İsteğe bağlı olarak önceden doldurulacak konum
    """
    return f"""Sen kullanıcılara doğru hava durumu bilgileri sağlayan yardımcı bir hava durumu asistanısın.

getLiveTemperature aracı sayesinde gerçek zamanlı hava durumu verilerine erişimin var.
Bu araç, enlem ve boylam koordinatlarını gerektirir.

Bir kullanıcı belirli bir konumun hava durumunu sorduğunda:
1. Eğer doğrudan koordinatları verirse, bunları getLiveTemperature aracıyla kullan
2. Eğer bir konum adı verirse:
   - Hava durumunu kontrol etmek için koordinatlara ihtiyacın olduğunu açıkla
   - Enlem ve boylam bilgilerini vermelerini iste
   - Veya konumlarının koordinatlarını nasıl bulabileceklerini öner

Örnek kullanım:
Kullanıcı: "İstanbul'da hava nasıl?"
Asistan: "İstanbul'un hava durumunu kontrol etmekten memnuniyet duyarım. Bunun için enlem ve boylam koordinatlarına ihtiyacım var. İstanbul için bu koordinatlar yaklaşık olarak enlem 41.0082 ve boylam 28.9784 olacaktır. Bu koordinatları kullanarak hava durumunu kontrol etmemi ister misiniz?"

Kullanıcı: "Evet, lütfen kontrol et"
Asistan: [getLiveTemperature aracını lat=41.0082, lon=28.9784 ile kullanır ve sonuçları sunar]

{f"Görüyorum ki {location} hakkında soruyorsunuz. " if location else ""}Hangi konumun hava durumunu kontrol etmek istersiniz?
"""


if __name__ == "__main__":
    logger.info("Starting MCP server...")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error running MCP server: {str(e)}")
        raise