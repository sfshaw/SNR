'''This module contains the core code for SNR, specifically concrete
 implementations of the protocols defined in `snr.protocol`.

The most important classes implemented include the `snr.core.node.Node`
event loop, base `snr.core.endpoint.Endpoint`, and
`snr.core.datastore.Datastore`. While most of the useful classes from this
module can be imported using `from snr import *`, a few are not included that
way and need to be imported separately.
'''
