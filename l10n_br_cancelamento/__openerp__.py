{
    "name": "Cancelamento NFE",
    "version": "1.0",
    "depends": ["base","account_cancel"],
    "author": "Danimar Ribeiro",
    'category': 'Localisation Brasil',
    'license': 'AGPL-3',
    'website': 'http://www.openerpbrasil.org',
    "description": """
      Este módulo é complementar para enviar para a receita a inutilização da numeração da nota.
      Dependencias: pysped, geraldo, pyxmlsec
      Instalando pyxmlsec 
        sudo pip install pyxmlsec
        Dependencias ->
        sudo apt-get install libxmlsec1-dev
        sudo apt-get install libxml2-dev
      Instalando geraldo
        sudo pip install geraldo
    """,
    'depends': [
        'l10n_br_account', 
        'account_cancel'       
    ],
    "init_xml": [],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}