a = ['glance_store', 'oslo.context', 'oslo.serialization', 'oslo.utils', 'oslosphinx', 'oslotest']

'''for i in a:
    if 'murano' or 'mistral' in i:
        print 'stackforge'
    else:
        print 'openstack'

        '''

if 'mistral' in a[1] or 'murano' in a[1]:
    print 'S'
else:
    print 'O'