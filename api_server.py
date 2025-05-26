from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from app import getliveTemp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='api_server.log')
logger = logging.getLogger('api_server')

# Initialize FastAPI app
app = FastAPI(
    title="Hava Durumu API",
    description="Gerçek zamanlı hava durumu bilgileri için API. Enlem ve boylam koordinatları kullanarak hava durumu verilerini alın.",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Response model
class WeatherResponse(BaseModel):
    temperature: float = None
    location: str = None
    country: str = None
    condition: str = None
    error: str = None

class CoordinatesRequest(BaseModel):
    latitude: float
    longitude: float

@app.get("/", response_class=HTMLResponse)
async def root():
    """Ana sayfa - API dokümantasyonuna yönlendirme"""
    return """
    <html>
        <head>
            <title>Hava Durumu API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 600px; margin: 0 auto; }
                .button { 
                    display: inline-block; 
                    padding: 10px 20px; 
                    margin: 10px; 
                    background-color: #007bff; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                }
                .button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌤️ Hava Durumu API</h1>
                <p>Gerçek zamanlı hava durumu bilgileri için API'mize hoş geldiniz!</p>
                
                <h2>📖 API Dokümantasyonu</h2>
                <a href="/docs" class="button">Swagger UI</a>
                <a href="/redoc" class="button">ReDoc</a>
                
                <h2>🔧 Kullanım</h2>
                <p>API'yi test etmek için Swagger UI'ı kullanın veya doğrudan endpoint'leri çağırın:</p>
                <ul>
                    <li><strong>GET /weather</strong> - Koordinatlarla hava durumu</li>
                    <li><strong>POST /weather</strong> - JSON ile hava durumu</li>
                </ul>
                
                <h2>📍 Örnek Koordinatlar</h2>
                <ul>
                    <li><strong>İstanbul:</strong> 41.0082, 28.9784</li>
                    <li><strong>Ankara:</strong> 39.9334, 32.8597</li>
                    <li><strong>İzmir:</strong> 38.4192, 27.1287</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.get("/weather", response_model=WeatherResponse, 
         summary="Hava Durumu Al (GET)",
         description="Enlem ve boylam koordinatları kullanarak gerçek zamanlı hava durumu bilgilerini alın.")
async def get_weather(
    lat: float = Query(..., description="Enlem koordinatı (örn: 41.0082)", example=41.0082),
    lon: float = Query(..., description="Boylam koordinatı (örn: 28.9784)", example=28.9784)
) -> WeatherResponse:
    """
    Koordinatlarla hava durumu bilgisi alın.
    
    - **lat**: Enlem koordinatı (-90 ile 90 arası)
    - **lon**: Boylam koordinatı (-180 ile 180 arası)
    """
    try:
        logger.info(f"GET request for coordinates: {lat}, {lon}")
        
        # Validate coordinates
        if not (-90 <= lat <= 90):
            raise HTTPException(status_code=400, detail="Enlem -90 ile 90 arasında olmalıdır")
        if not (-180 <= lon <= 180):
            raise HTTPException(status_code=400, detail="Boylam -180 ile 180 arasında olmalıdır")
        
        result = getliveTemp(lat, lon)
        logger.info(f"Result: {result}")
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return WeatherResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_weather: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")

@app.post("/weather", response_model=WeatherResponse,
          summary="Hava Durumu Al (POST)",
          description="JSON formatında koordinatlar göndererek hava durumu bilgilerini alın.")
async def post_weather(coordinates: CoordinatesRequest) -> WeatherResponse:
    """
    JSON ile hava durumu bilgisi alın.
    
    Request body:
    ```json
    {
        "latitude": 41.0082,
        "longitude": 28.9784
    }
    ```
    """
    try:
        logger.info(f"POST request for coordinates: {coordinates.latitude}, {coordinates.longitude}")
        
        # Validate coordinates
        if not (-90 <= coordinates.latitude <= 90):
            raise HTTPException(status_code=400, detail="Enlem -90 ile 90 arasında olmalıdır")
        if not (-180 <= coordinates.longitude <= 180):
            raise HTTPException(status_code=400, detail="Boylam -180 ile 180 arasında olmalıdır")
        
        result = getliveTemp(coordinates.latitude, coordinates.longitude)
        logger.info(f"Result: {result}")
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return WeatherResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in post_weather: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")

@app.get("/health")
async def health_check():
    """Sunucu sağlık kontrolü"""
    return {"status": "healthy", "message": "API çalışıyor"}

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
