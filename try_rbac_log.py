#Tribe 1 details:
Tribe1 = {
    'asset': {
        'data': {
            'data': {
                'link': 'bfc131382f579aaf29107c26dcafb1e1e2d096257126870df1f0a4b28004fa49', 
                'name': 'tribe1', 
                'ns': 'rbac-bdb-demo.tribe1'
            }, 
            'link': 'bfc131382f579aaf29107c26dcafb1e1e2d096257126870df1f0a4b28004fa49', 
            'name': 'tribe1', 
            'ns': 'rbac-bdb-demo.tribe1'
        }
    }, 
    'id': '1e2292e507568bba46dd7ae193f68b6ceb9d24fc301fc79577287f54254ec6fb', 
    'inputs': [
        {
            'fulfillment': 'pGSAIDqXf6H35SCWdMsNCYOJ2LsmGRCt3AariQZ-H93kSSZUgUBa4AxqeHmTL2vR1zyOXRfG15UsEVmp42XVeFLz1bBZNOV8J3hTpdTysgpgvugypWmqg08335MUL-qqCs7HkCID', 
            'fulfills': None, 
            'owners_before': [
                '4widgxqwn3mFC7vxS7cCp7d3dPGqZQSPhdwqGr5Njw87'
            ]
        }
    ],
    'metadata': {
        'can_link': '806af584b35025fbb47b2f76b43b336224fbf0874ec41830f623485a3876940d'
    }, 
    'operation': 'CREATE', 
    'outputs': [
        {
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': '4widgxqwn3mFC7vxS7cCp7d3dPGqZQSPhdwqGr5Njw87', 
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;8G4K2YbLIysYuV60IvzBeeWOfw_R6fYz1HxS9gFNCa0?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': [
                '4widgxqwn3mFC7vxS7cCp7d3dPGqZQSPhdwqGr5Njw87'
            ]
        }
    ], 
    'version': '2.0'
}

#user1 details
User1 = {
    'asset': {
        'data': {
            'createdBy': 'Fzj4qnHXPTu6smVaGWuFgEUKSWwH3yjgRjEjL9HEoqnc', 
            'data': {
                'createdBy': 'Fzj4qnHXPTu6smVaGWuFgEUKSWwH3yjgRjEjL9HEoqnc', 
                'keyword': 'UserAsset', 
                'link': '0c398fb6e02c02683b49e20eef35344e791f876d0d5e43afdd2958c019b12240', 
                'ns': 'rbac-bdb-demo.tribe1', 
                'type': 'tribe1'
            }, 
            'keyword': 'UserAsset', 
            'link': '0c398fb6e02c02683b49e20eef35344e791f876d0d5e43afdd2958c019b12240', 
            'ns': 'rbac-bdb-demo.tribe1', 
            'type': 'tribe1'
        }
    }, 
    'id': '31e6020f5cc5e1a2c353a3c9548499cae8894e2dbc59b63c7c76a1de1527918a', 
    'inputs': [
        {
            'fulfillment': 'pGSAIN7NSZrOh6ehXVlDsiBCg1mXB4BSv5Okq-dG2755uWWVgUBI-GZLcTuEFKZWi8mF36ziJGWutuyerYgtxrJrze1OiQbQs0Q1KMTW7vWHsuCKO0fUnUlZ-TKuLvhSOa7jEYMN', 
            'fulfills': None, 
            'owners_before': ['Fzj4qnHXPTu6smVaGWuFgEUKSWwH3yjgRjEjL9HEoqnc']
        }
    ], 
    'metadata': {
        'event': 'User Assigned',
        'eventData': {
            'userType': 'tribe1'
        }, 
        'publicKey': 'Fzj4qnHXPTu6smVaGWuFgEUKSWwH3yjgRjEjL9HEoqnc',
        'timestamp': '04/07/2021 11:41:04'
    }, 
    'operation': 'CREATE', 
    'outputs': [
        {
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': 'Fzj4qnHXPTu6smVaGWuFgEUKSWwH3yjgRjEjL9HEoqnc', 
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;bJwN731N_7cY3_gQNEQTPid00xeaPTt015YsrjKj9a4?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': ['Fzj4qnHXPTu6smVaGWuFgEUKSWwH3yjgRjEjL9HEoqnc']
        }
    ], 
    'version': '2.0'
}