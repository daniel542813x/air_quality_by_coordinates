from fastapi import WebSocket


#reference: https://medium.com/@nmjoshi/getting-started-websocket-with-fastapi-b41d244a2799
class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)
        
def is_validate_air_quality_params(air_params):
    required_params = ["latitude", "longitude", "type_gas", "forecast_days"]
    
    for param in required_params:
        if param not in air_params: 
            return False
        
    return True
        
    
    
    