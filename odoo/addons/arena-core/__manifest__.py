{
    'name': 'Arena Core',
    'version': '1.0',
    'author': 'RDB Software Foundation',
    'category': 'Tools',
    'depends': [
        'base',
        'web',
    ],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/arena_model_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
