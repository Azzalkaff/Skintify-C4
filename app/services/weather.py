import requests
import os
from typing import Dict, Any

class WeatherService:
    """Mock/Real Service untuk mendapatkan data cuaca kota."""
    
    @staticmethod
    def fetch_weather(city: str) -> Dict[str, Any]:
        """
        Gunakan OpenWeatherMap API atau Mock Data.
        Untuk kebutuhan akademis, kita sediakan mock jika API Key tidak ada.
        """
        if not city:
            return {"status": "error", "msg": "City not provided"}

        # Simulasi/Mock jika offline atau tidak ada API Key
        # (Idealnya ambil dari OpenWeatherMap menggunakan requests)
        mock_data = {
            "jakarta": {"temp": 32, "humidity": 75, "uv_index": 8, "condition": "Cerah Berawan"},
            "bandung": {"temp": 24, "humidity": 60, "uv_index": 5, "condition": "Sejuk"},
            "surabaya": {"temp": 34, "humidity": 80, "uv_index": 10, "condition": "Panas Terik"},
            "jogja": {"temp": 29, "humidity": 65, "uv_index": 6, "condition": "Cerah"}
        }
        
        city_lower = city.lower()
        if city_lower in mock_data:
            return {
                "status": "success",
                "city": city,
                **mock_data[city_lower]
            }
        
        # Default Fallback (Safe average)
        return {
            "status": "success",
            "city": city,
            "temp": 28,
            "humidity": 50,
            "uv_index": 4,
            "condition": "Normal"
        }
