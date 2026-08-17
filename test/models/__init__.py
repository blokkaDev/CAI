import json

class Models:
    def __init__(self):
        self.list= {}

    def load(self, path="models/models.json"):
        with open(file=path, mode="r", encoding="UTF-8") as file:
            self.list= json.load(file)
        
            return {
                "success": True, 
                "message": "Models loaded successfully!"
            }