{
    'name': 'Agendamento Core',
    'version': '1.0',
    'author': 'RDB Software Foundation',
    'category': 'Tools',
    'depends': [
        'base',
        'web',
        'mail',
        'base_address_extended'
    ],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/scheduler_model_views.xml',
        'views/procedimento_views.xml',
        'views/configuracao_funcionamento_views.xml',
        'views/res_partner_views.xml',
        'views/estacao_views.xml',
        'views/agendamento_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
