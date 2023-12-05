import enum

class OrderStatus(enum.Enum):
    Criado = "Criado"
    Confirmado = "Confirmado"
    Despachado = "Despachado"
    Entregue = "Entregue"
    Avaliado = "Avaliado"
    
    def to_dict(self):
        return {"value": self.value}