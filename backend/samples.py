import random

SCHOOLS_MAPS = [ \
    {
        "name": "Escola Primária Sol Nascente",
        "address": "Rua das Flores, 123",
        "cep": "12345-678",
        "cnpj": "12.345.678/0001-12"
    },
    {
        "name": "Colégio Estadual Rio Branco",
        "address": "Av. Central, 456",
        "cep": "23456-789",
        "cnpj": "23.456.789/0001-23"
    },
    {
        "name": "Instituto Educacional Verdes Campos",
        "address": "Rua das Palmeiras, 789",
        "cep": "34567-890",
        "cnpj": "34.567.890/0001-34"
    },
    {
        "name": "Escola Tecnológica Futuro Brilhante",
        "address": "Av. Tecnológica, 101",
        "cep": "45678-901",
        "cnpj": "45.678.901/0001-45"
    },
    {
        "name": "Centro Educacional Nova Era",
        "address": "Rua Nova Era, 202",
        "cep": "56789-012",
        "cnpj": "56.789.012/0001-56"
    }
]

SUPPLIERS_MAPS = [ \
    {
        "name": "Papelaria ABC",
        "address": "Rua dos Estudantes, 303",
        "cep": "67890-123",
        "cnpj": "67.890.123/0001-67"
    },
    {
        "name": "Livraria Educar",
        "address": "Av. dos Livros, 404",
        "cep": "78901-234",
        "cnpj": "78.901.234/0001-78"
    },
    {
        "name": "Distribuidora de Material Escolar Soluções",
        "address": "Rua do Saber, 505",
        "cep": "89012-345",
        "cnpj": "89.012.345/0001-89"
    },
    {
        "name": "Tecnologia Educacional TechEdu",
        "address": "Av. da Inovação, 606",
        "cep": "90123-456",
        "cnpj": "90.123.456/0001-90"
    },
    {
        "name": "Equipamentos Escolares EquipEdu",
        "address": "Rua dos Professores, 707",
        "cep": "01234-567",
        "cnpj": "01.234.567/0001-01"
    }
]


TRANSPORTERS_MAPS = [ \
    {
        "name": "Transportes Rápidos",
        "address": "Rua Veloz, 808",
        "cep": "12345-678",
        "cnpj": "12.345.678/0002-12"
    },
    {
        "name": "Entregas Seguras",
        "address": "Av. Segurança, 909",
        "cep": "23456-789",
        "cnpj": "23.456.789/0002-23"
    },
    {
        "name": "Logística Eficiente",
        "address": "Rua da Agilidade, 1010",
        "cep": "34567-890",
        "cnpj": "34.567.890/0002-34"
    },
    {
        "name": "Distribuição Expressa",
        "address": "Av. Rápida, 1111",
        "cep": "45678-901",
        "cnpj": "45.678.901/0002-45"
    },
    {
        "name": "Transportes Confiáveis",
        "address": "Rua da Confiança, 1212",
        "cep": "56789-012",
        "cnpj": "56.789.012/0002-56"
    }
]

EMPLOYES_SEDUC_MAPS = [ \
    {
        "name": "João Silva",
        "cpf": "123.456.789-00",
        "email": "joaosilva@seduc.learnlink.com.br",
        "password": "senha123",
        "role": "Coordenador Pedagógico",
        "celular": "(11) 98765-4321"
    },
    {
        "name": "Maria Oliveira",
        "cpf": "987.654.321-00",
        "email": "mariaoliveira@seduc.learnlink.com.br",
        "password": "senha321",
        "role": "Diretor Administrativo",
        "celular": "(11) 97654-3210"
    }
]

EMPLOYES_SCHOOL_MAPS = [ \
{
        "name": "Carlos Pereira",
        "cpf": "234.567.890-11",
        "email": "carlospereira@school.learnlink.com.br",
        "password": "escola123",
        "school_id": 3
    },
    {
        "name": "Ana Beatriz",
        "cpf": "876.543.210-11",
        "email": "anabeatriz@school.learnlink.com.br",
        "password": "escola321",
        "school_id": 2
    }
]

EMPLOYES_SUPPLIER_MAPS = [ \
    {
        "name": "Ricardo Mendes",
        "cpf": "345.678.901-22",
        "email": "ricardomendes@supplier.learnlink.com.br",
        "password": "fornecedor123",
        "supplier_id": 1
    },
    {
        "name": "Fernanda Gomes",
        "cpf": "765.432.109-22",
        "email": "fernandagomes@supplier.learnlink.com.br",
        "password": "fornecedor321",
        "supplier_id": 2
    }
]


EMPLOYES_TRANSPORTER_MAPS = [ \
    {
        "name": "Roberto Carvalho",
        "cpf": "456.789.012-33",
        "email": "robertocarvalho@transporter.learnlink.com.br",
        "password": "transporte123",
        "transporter_id": 1,
        "celular": "(11) 95432-6789"
    },
    {
        "name": "Juliana Martins",
        "cpf": "654.321.098-33",
        "email": "julianamartins@transporter.learnlink.com.br",
        "password": "transporte321",
        "transporter_id": 2,
        "celular": "(11) 93210-8765"
    }
]



ORDERS_MAPS = [ \
    {"id": 1, "supplier_id": 1, "transporter_id": 1, "school_id": 1, "status": "Criado", "amount": 1000.00, "nf": "NF001", "nr": "NR001", "purchase_date": "2023-01-01", "employe_seduc_id": 1},
    {"id": 2, "supplier_id": 2, "transporter_id": 2, "school_id": 2, "status": "Confirmado", "amount": 1500.00, "nf": "NF002", "nr": "NR002", "purchase_date": "2023-01-05", "employe_seduc_id": 2},
    {"id": 3, "supplier_id": 3, "transporter_id": 3, "school_id": 3, "status": "Despachado", "amount": 2000.00, "nf": "NF003", "nr": "NR003", "purchase_date": "2023-01-10", "employe_seduc_id": 1},
    {"id": 4, "supplier_id": 4, "transporter_id": 4, "school_id": 4, "status": "Entregue", "amount": 2500.00, "nf": "NF004", "nr": "NR004", "purchase_date": "2023-01-15", "employe_seduc_id": 2},
    {"id": 5, "supplier_id": 5, "transporter_id": 5, "school_id": 5, "status": "Avaliado", "amount": 3000.00, "nf": "NF005", "nr": "NR005", "purchase_date": "2023-01-20", "employe_seduc_id": 1},
    {"id": 6, "supplier_id": 1, "transporter_id": 1, "school_id": 1, "status": "Criado", "amount": 3500.00, "nf": "NF006", "nr": "NR006", "purchase_date": "2023-01-25", "employe_seduc_id": 2},
    {"id": 7, "supplier_id": 1, "transporter_id": 1, "school_id": 1, "status": "Criado", "amount": 4000.00, "nf": "NF007", "nr": "NR007", "purchase_date": "2023-03-05", "employe_seduc_id": 1},
    {"id": 8, "supplier_id": 2, "transporter_id": 2, "school_id": 2, "status": "Confirmado", "amount": 4500.00, "nf": "NF008", "nr": "NR008", "purchase_date": "2023-03-10", "employe_seduc_id": 2},
    {"id": 9, "supplier_id": 3, "transporter_id": 3, "school_id": 3, "status": "Despachado", "amount": 5000.00, "nf": "NF009", "nr": "NR009", "purchase_date": "2023-03-15", "employe_seduc_id": 1},
    {"id": 10, "supplier_id": 4, "transporter_id": 4, "school_id": 4, "status": "Entregue", "amount": 5500.00, "nf": "NF010", "nr": "NR010", "purchase_date": "2023-03-20", "employe_seduc_id": 2},
    {"id": 11, "supplier_id": 5, "transporter_id": 5, "school_id": 5, "status": "Avaliado", "amount": 6000.00, "nf": "NF011", "nr": "NR011", "purchase_date": "2023-03-25", "employe_seduc_id": 1},
    {"id": 12, "supplier_id": 1, "transporter_id": 1, "school_id": 1, "status": "Criado", "amount": 6500.00, "nf": "NF012", "nr": "NR012", "purchase_date": "2023-03-30", "employe_seduc_id": 2},
    {"id": 13, "supplier_id": 2, "transporter_id": 2, "school_id": 2, "status": "Confirmado", "amount": 7000.00, "nf": "NF013", "nr": "NR013", "purchase_date": "2023-04-05", "employe_seduc_id": 1},
    {"id": 14, "supplier_id": 3, "transporter_id": 3, "school_id": 3, "status": "Despachado", "amount": 7500.00, "nf": "NF014", "nr": "NR014", "purchase_date": "2023-04-10", "employe_seduc_id": 2},
    {"id": 15, "supplier_id": 4, "transporter_id": 4, "school_id": 4, "status": "Entregue", "amount": 8000.00, "nf": "NF015", "nr": "NR015", "purchase_date": "2023-04-15", "employe_seduc_id": 1},
    {"id": 16, "supplier_id": 5, "transporter_id": 5, "school_id": 5, "status": "Avaliado", "amount": 8500.00, "nf": "NF016", "nr": "NR016", "purchase_date": "2023-04-20", "employe_seduc_id": 2},
    {"id": 17, "supplier_id": 1, "transporter_id": 1, "school_id": 1, "status": "Criado", "amount": 9000.00, "nf": "NF017", "nr": "NR017", "purchase_date": "2023-04-25", "employe_seduc_id": 1},
    {"id": 18, "supplier_id": 2, "transporter_id": 2, "school_id": 2, "status": "Confirmado", "amount": 9500.00, "nf": "NF018", "nr": "NR018", "purchase_date": "2023-04-30", "employe_seduc_id": 2},
    {"id": 19, "supplier_id": 3, "transporter_id": 3, "school_id": 3, "status": "Despachado", "amount": 10000.00, "nf": "NF019", "nr": "NR019", "purchase_date": "2023-05-05", "employe_seduc_id": 1},
    {"id": 20, "supplier_id": 5, "transporter_id": 5, "school_id": 5, "status": "Avaliado", "amount": 5500.00, "nf": "NF020", "nr": "NR020", "purchase_date": "2023-02-28", "employe_seduc_id": 2}
]
