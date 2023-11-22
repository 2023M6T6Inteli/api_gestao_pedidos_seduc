import enum

class OrderStatus(enum.Enum):
    Criado = "Criado"
    Confirmado = "Confirmado"
    Em_Transito = "Em Trânsito"
    Entregue = "Entregue"
    Avaliado = "Avaliado"