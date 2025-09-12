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
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/procedimento_views.xml',
        'views/configuracao_funcionamento_views.xml',
        'views/res_partner_views.xml',
        'views/recurso_views.xml',
        'views/agendamento_views.xml',
        'views/ordem_servico_views.xml',
        'views/material_views.xml',
        'wizard/views/gerar_os_wizard.xml',
        'views/menu.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "/scheduler_core/static/lib/inputmask/inputmask.min.js",
            "/scheduler_core/static/src/js/field_mask.js",
        ],
    },
    'installable': True,
    'application': True,
}
