#!/usr/bin/python

import os
import sys
import numpy as np

sys.path[:0] = (os.path.abspath(os.path.dirname(sys.argv[0])) + "/../lib",)

import vnlog
import cStringIO

inputstring = '''#! zxcv
# time height
## qewr
1 2
3 4
# - 10
- 5
6 -
- -
7 8
'''

ref = r'''1 2
3 4
None 5
6 None
None None
7 8
'''

f = cStringIO.StringIO(inputstring)

parser = vnlog.vnlog()
resultstring = ''
for l in f:
    parser.parse(l)
    d = parser.values_dict()
    if not d:
        continue
    resultstring += '{} {}\n'.format(d['time'],d['height'])

if resultstring != ref:
    print "Expected '{}' but got '{}'".format(ref, resultstring)
    print "Test failed!"
    sys.exit(1)




f = cStringIO.StringIO(inputstring)

resultstring = ''
for d in vnlog.vnlog('/tmp/tst.vnl'):
    resultstring += '{} {}\n'.format(d['time'],d['height'])
if resultstring != ref:
    print "Expected '{}' but got '{}'".format(ref, resultstring)
    print "Test failed!"
    sys.exit(1)



inputstring_noundef = r'''#! zxcv
# time height
## qewr
1 2
3 4
# - 10
7 8
'''
ref_noundef = np.array(((1,2),(3,4),(7,8)))
f = cStringIO.StringIO(inputstring_noundef)
log_numpy_array,list_keys,dict_key_index = vnlog.slurp(f)
if np.linalg.norm((ref_noundef - log_numpy_array).ravel()) > 1e-8:
    raise Exception("Array mismatch: expected '{}' but got '{}". \
                    format(ref_noundef, log_numpy_array))
if len(list_keys) != 2 or list_keys[0] != 'time' or list_keys[1] != 'height':
    raise Exception("Key mismatch: expected '{}' but got '{}". \
                    format(('time','height'), list_keys))
if len(dict_key_index) != 2 or dict_key_index['time'] != 0 or dict_key_index['height'] != 1:
    raise Exception("Key-dict mismatch: expected '{}' but got '{}". \
                   format({'time': 0, 'height': 1}, dict_key_index))



print "Test passed";
sys.exit(0);
