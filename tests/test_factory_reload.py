from typing import Union

from snr import *

from .test_reload import mod_a, mod_b

EndpointUnion = Union[mod_a.EndpointUnderTest,
                      mod_b.EndpointUnderTest]


class FactoryUnderTest(EndpointFactory):
    def __init__(self,
                 expector: ExpectorProtocol,
                 ) -> None:
        super().__init__(mod_a)
        self.target = mod_a.EndpointUnderTest
        self.expector = expector

    def get(self, parent: NodeProtocol) -> Union[mod_a.EndpointUnderTest,
                                                 mod_b.EndpointUnderTest]:
        return self.target(self, parent, self.expector)


class TestFactoryReload(SNRTestCase):
    def test_factory_swap(self):
        '''This test does not test importlib
        '''
        with OrderedExpector(["mod_a", "mod_b", "mod_a"], self) as expector:
            node = self.mock_node()
            fac = FactoryUnderTest(expector)
            endpoint = fac.get(node)
            endpoint.call()
            fac.reload_targets = [mod_b]
            fac.target = mod_b.EndpointUnderTest  # type: ignore
            fac.reload()
            endpoint = fac.get(node)
            endpoint.call()
            fac.reload_targets = [mod_a]
            fac.target = mod_a.EndpointUnderTest  # type: ignore
            fac.reload()
            endpoint = fac.get(node)
            endpoint.call()
