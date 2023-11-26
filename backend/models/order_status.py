import enum

class OrderStatus(enum.Enum):
    Criado = "Criado"
    Confirmado = "Confirmado"
    Em_Transito = "Em Trânsito"
    Entregue = "Entregue"
    Avaliado = "Avaliado"
    
    def to_dict(self):
        return {"value": self.value}