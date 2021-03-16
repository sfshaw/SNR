import multiprocessing as mp
import socket
import time

import pytest
from snr import *


class TestSocketsLsitener(SNRTestCase):

    @pytest.mark.timeout(0.200)
    def test_sockets_listener_recv(self) -> None:

        data_key = "my_data"
        page = Page(data_key, "data", "origin", 0.75)
        expectations: TaskExpectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector[TaskId](expectations, self) as expector, \
                self.create_server(("localhost", 0)) as server_socket:
            port: int = server_socket.getsockname()[1]
            factories = [
                SocketsListenerFactory((server_socket, port)),
                ExpectorEndpointFactory(expector,
                                        exit_when_satisfied=True),
            ]
            proc = mp.Process(target=self.run_test_node,
                              args=(factories,))
            proc.start()
            time.sleep(0.010)
            with socket.create_connection(("localhost", port)) as client:
                sock = SocketsWrapper((client, None),
                                      self.get_context())
                sock.send(page.serialize())

            proc.join(0.100)
            try:
                self.assertFalse(proc.is_alive())
            except AssertionError as e:
                proc.terminate()
                raise e

    @pytest.mark.timeout(0.200)
    def test_sockets_listener_send(self) -> None:

        data_key = "my_data"
        page = Page(data_key, "data", "origin", 0.75)
        expectations: TaskExpectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector[TaskId](expectations, self) as expector, \
                self.create_server(("", 0)) as server_socket:
            port = server_socket.getsockname()[1]
            factories = [
                SocketsListenerFactory((server_socket, port),
                                       [data_key]),
                ExpectorEndpointFactory(expector,
                                        exit_when_satisfied=True),
            ]
            proc = mp.Process(target=self.run_test_node,
                              args=(factories,))
            proc.start()
            time.sleep(0.010)
            with socket.create_connection(("localhost", port)) as client:
                sock = SocketsWrapper((client, ("", port)), self.get_context())
                sock.send(page.serialize())
                response = sock.recv()
                assert response
                self.assertPage(Page.deserialize(response),
                                page.key,
                                page.data,
                                page.origin,
                                page.created_at_s,
                                page.process)

            proc.join(0.100)
            try:
                self.assertFalse(proc.is_alive())
            except AssertionError as e:
                proc.terminate()
                raise e
