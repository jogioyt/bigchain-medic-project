def getAdminType():
    admin_type = {
        'asset': {
            'data': {
                'name': 'admin', 
                'ns': 'medical-app.admin'
            }
        }, 
        'id': '84554f1477196fbaf9181aacf8c6f545d63172ed439ddbb890226e91df1afe2c', 
        'inputs': [{
            'fulfillment': 'pGSAIME_B_2WhVJ4Hgd2A-yNQAU32Ngo4Gw6OCn3DlQZJEt6gUAKBgipbo6uS5GkG-aBdHk6lypUvRMAWhJyyL1QjKEfYHJBYhxbUyB1G1OXIPaBx85AdXcBw3GIOE77bl7LZhIB', 
            'fulfills': None, 
            'owners_before': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'metadata': {
            'can_link': 'E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd'
        }, 
        'operation': 'CREATE',
        'outputs': [{
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': 'E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd', 
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;OpspvyRB0dyQvrLE3MXnhox7seFMOxQ3jkmOFXFTKNo?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'version': '2.0'
    }
    return admin_type

def getApp():
    app_tx = {
        'asset': {
            'data': {
                'name': 'medical-app', 
                'ns': 'medical-app'
            }
        }, 
        'id': '7a1a973fb01e54007b317772f29752565f03753c8f1540bbf5d17abaf23270da', 
        'inputs': [{
            'fulfillment': 'pGSAIME_B_2WhVJ4Hgd2A-yNQAU32Ngo4Gw6OCn3DlQZJEt6gUDLxcyCstu4DlLdYdHp5ymMbOuwMxiT8FSmc1KlzdAF_uyjX71Yi4JCHjrUCHlxOvJ5FPI3aEVy7fFdrEA9LuIO',
            'fulfills': None,
            'owners_before': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'metadata': {
            'can_link': '84554f1477196fbaf9181aacf8c6f545d63172ed439ddbb890226e91df1afe2c'
        }, 
        'operation': 'CREATE',
        'outputs': [{
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': 'E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd', 
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;OpspvyRB0dyQvrLE3MXnhox7seFMOxQ3jkmOFXFTKNo?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'version': '2.0'
    }
    return app_tx

def getHospitalType():
    hospital_type = {
        'asset': {
            'data': {
                'link': '7a1a973fb01e54007b317772f29752565f03753c8f1540bbf5d17abaf23270da', 
                'name': 'hospital', 
                'ns': 'medical-app.hospital'
            }
        }, 
        'id': '1713f8eea54c7f0507e51baaa0eddff088b097aeb9ec0f88ea5f09563b99dc7a', 
        'inputs': [{
            'fulfillment': 'pGSAIME_B_2WhVJ4Hgd2A-yNQAU32Ngo4Gw6OCn3DlQZJEt6gUBZqWBnn6EoFwlWivZmYchY5W6xVQ7GNMf0JBkrcsPkno14g7FLx3WDMRAowTuvo9cTclkAgue9OCsC5HDdjbIG', 
            'fulfills': None, 
            'owners_before': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'metadata': {
            'can_link': '84554f1477196fbaf9181aacf8c6f545d63172ed439ddbb890226e91df1afe2c'
        }, 
        'operation': 'CREATE', 
        'outputs': [{
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': 'E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd', 
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;OpspvyRB0dyQvrLE3MXnhox7seFMOxQ3jkmOFXFTKNo?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'version': '2.0'
    }
    return hospital_type

def getDoctorType():
    doctor_type = {
        'asset': {
            'data': {
                'link': '7a1a973fb01e54007b317772f29752565f03753c8f1540bbf5d17abaf23270da',
                'name': 'doctors', 
                'ns': 'medical-app.doctors'
            }
        }, 
        'id': 'c95db467fa33624ecd8151e52a4179892dc7fbfc94e5ef23c609a171454d0463', 
        'inputs': [{
            'fulfillment': 'pGSAIME_B_2WhVJ4Hgd2A-yNQAU32Ngo4Gw6OCn3DlQZJEt6gUDWM0BBzmDrgFErHXDKVoJRmfKuQKwmxiiQ5iuxO-Lq7NNXBrjPaIPGETKoaS7_O64EYGuOv7wn9xO_QWqpUwYC', 
            'fulfills': None, 
            'owners_before': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'metadata': {
            'can_link': '1713f8eea54c7f0507e51baaa0eddff088b097aeb9ec0f88ea5f09563b99dc7a'
        }, 
        'operation': 'CREATE',
        'outputs': [{
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': 'E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd',
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;OpspvyRB0dyQvrLE3MXnhox7seFMOxQ3jkmOFXFTKNo?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }],
        'version': '2.0'
    }
    return doctor_type

def getPatientType():
    patient_type = {
        'asset': {
            'data': {
                'link': '7a1a973fb01e54007b317772f29752565f03753c8f1540bbf5d17abaf23270da', 
                'name': 'patient', 
                'ns': 'medical-app.patient'
            }
        }, 
        'id': '871b1725889d28bab3c1fe5a03c12343109d7bfc72ac1e8d8e3482192ad1df60', 
        'inputs': [{
            'fulfillment': 'pGSAIME_B_2WhVJ4Hgd2A-yNQAU32Ngo4Gw6OCn3DlQZJEt6gUCbtOqeywKJM5xzHC8mhF_NXoha4H1moBPQ2dCegr8ie0oQCRKiGypSExSSGj3_IelQ3r0rE2Hz1QzTJ-209ZkA', 
            'fulfills': None, 
            'owners_before': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'metadata': {
            'can_link': 'c95db467fa33624ecd8151e52a4179892dc7fbfc94e5ef23c609a171454d0463'
        }, 
        'operation': 'CREATE',
        'outputs': [{
            'amount': '1', 
            'condition': {
                'details': {
                    'public_key': 'E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd', 
                    'type': 'ed25519-sha-256'
                }, 
                'uri': 'ni:///sha-256;OpspvyRB0dyQvrLE3MXnhox7seFMOxQ3jkmOFXFTKNo?fpt=ed25519-sha-256&cost=131072'
            }, 
            'public_keys': ['E1MRzBmUP8qsxH2Sbv6wSxgf1a3q3hHeLDohAshseVCd']
        }], 
        'version': '2.0'
    }
    return patient_type