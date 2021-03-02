import multiprocessing as mp

import pytest
from snr import *


class TestPipeLoop(SNRTestCase):

    @pytest.mark.timeout(50)
    def test_pipe_noop(self) -> None:

        pipe = mp.Pipe(duplex=True)

        self.run_test_node([
            PipeLoopFactory(pipe[0]),
            TimeoutLoopFactory(ms=1),
        ])
        self.assertTrue(pipe[1].poll(0.005))
        self.assertRaises(EOFError, lambda: pipe[1].recv())

    @pytest.mark.timeout(200)
    def test_one_pipe(self) -> None:

        data_key = "my_data"
        expectations: Expectations = {
            (TaskType.process_data, data_key): 1
        }

        with self.expector(expectations) as expector:

            (pipe_in, pipe_out) = mp.Pipe(duplex=True)
            pipe_in.send(Page(data_key, "some data", "test", 0).serialize())
            pipe_in.close()
            self.run_test_node([
                PipeLoopFactory(pipe_out),
                ExpectorEndpointFactory(expector,
                                        exit_when_satisfied=True),
            ])

    @pytest.mark.timeout(500)
    def test_two_pipe_loops(self) -> None:
        # logging.getLogger().setLevel(logging.WARNING)

        data_key = "my_data"
        expectations: Expectations = {
            (TaskType.process_data, data_key): 1
        }

        with MPExpector(expectations, self) as expector1, \
            MPExpector(expectations, self) as expector2, \
                self.temp_file() as temp_file:

            with temp_file.open() as f:
                f.write("some_data\n")

            temp_file.assertExists()

            (pipe1, pipe2) = mp.Pipe(duplex=True)
            config = Config(
                Mode.TEST, {
                    "test1": [
                        TextReplayerFactory(temp_file.path, data_key),
                        PipeLoopFactory(pipe1, [data_key]),
                        ExpectorEndpointFactory(expector1,
                                                exit_when_satisfied=True),
                    ],
                    "test2": [
                        PipeLoopFactory(pipe2),
                        ExpectorEndpointFactory(expector2,
                                                exit_when_satisfied=True),
                    ]})
            runner: MultiRunnerProtocol = MultiProcRunner(config,
                                                          ["test1", "test2"])
            runner.run()


if __name__ == '__main__':
    unittest.main()
