import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
import multiprocessing
import logging
import sys
import time

MAX_WORKERS = 5


# I/O BOUND
class ThreadsGenerator:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.loop = None
        self.future = None

    def execute_function(self, function_to_execute, *args):
        self.loop = asyncio.get_event_loop()
        event = asyncio.Event()
        self.future = self.loop.run_in_executor(self.executor, function_to_execute, event)

        return self.future

    def terminate(self):
        for p in self._working | self._free:
            p.terminate()
        self._free.clear()


# CPU BOUND
class CancellablePool:
    def __init__(self, max_workers=3):
        self._free = {self._new_pool() for _ in range(max_workers)}
        self._working = set()
        self._change = asyncio.Event()

    def _new_pool(self):
        return multiprocessing.Pool(1)

    async def apply(self, fn, *args):
        """
        Like multiprocessing.Pool.apply_async, but:
         * is an asyncio coroutine
         * terminates the process if cancelled
        """
        while not self._free:
            await self._change.wait()
            self._change.clear()
        pool = usable_pool = self._free.pop()
        self._working.add(pool)

        loop = asyncio.get_event_loop()
        fut = loop.create_future()

        def _on_done(obj):
            loop.call_soon_threadsafe(fut.set_result, obj)

        def _on_err(err):
            loop.call_soon_threadsafe(fut.set_exception, err)

        pool.apply_async(fn, args, callback=_on_done, error_callback=_on_err)

        try:
            return await fut
        except asyncio.CancelledError:
            pool.terminate()
            usable_pool = self._new_pool()
        finally:
            self._working.remove(pool)
            self._free.add(usable_pool)
            self._change.set()

    def shutdown(self):
        for p in self._working | self._free:
            p.terminate()
        self._free.clear()


"""

def blocks(n):
    log = logging.getLogger('blocks({})'.format(n))
    log.info('running')
    time.sleep(0.1)
    log.info('done')
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocks, i)
        for i in range(6)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


if __name__ == '__main__':
    # Configure logging to show the name of the thread
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited thread pool.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=3,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()
        
        
"""

"""

    async def accept_client(self, reader, writer):
        # loop = asyncio.get_running_loop()
        # with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while not writer.is_closing():

            data = await reader.read(MAX_LEN)
            msg = data.decode()

            # get information about socket
            info = writer.get_extra_info('socket')

            in_port = info.getsockname()[1]
            malicious_ip = info.getpeername()[0]

            print(f"Received something on: {in_port}, from {malicious_ip!r}")
            for name, param in self.Conns.items():
                if name == "Endlessh" and in_port in param[0]:
                    print("Enable Endlessh..\n")
                    # loop.run_in_executor(executor, Endlessh().run(writer, in_port, malicious_ip, msg, param[1]))
                    # executor.submit(Endlessh().run, writer, in_port, malicious_ip, msg, param[1])
                    await Endlessh().run(writer, in_port, malicious_ip, msg, param[1])
                    # await t.run(writer, in_port, malicious_ip, msg, param[1])
                    # loop.create_task(t.run(writer, in_port, malicious_ip, msg, param[1]))
                    # await loop.run_in_executor(executor, t.run, writer, in_port, malicious_ip, msg, param[1])

                if name == "Invisiport" and in_port in param[0]:
                    print("Enable Invisiport..\n")
                    # asyncio.run(Invisiport().run(writer, in_port, malicious_ip, msg, param[1]))
                    # executor.submit(Invisiport, writer, in_port, malicious_ip, msg, param[1])
                    await Invisiport().run(writer, in_port, malicious_ip, msg, param[1])
                    # await t.run(writer, in_port, malicious_ip, msg, param[1])
                    # await loop.run_in_executor(executor, t.run, writer, in_port, malicious_ip, msg, param[1])
                    # loop.create_task(t.run(writer, in_port, malicious_ip, msg, param[1]))
                if name == "Honeyports" and in_port in param[0]:
                    print("Enable Honeyports..\n")
                    await Honeyports().run(writer, malicious_ip, msg)
                if name == "Portspoof" and in_port in param[0]:
                    print("Enable Portspoof..\n")
                    await Portspoof(in_port).run(writer, malicious_ip, msg)
                if name == "Tcprooter":
                    print("Enable Tcprooter..\n")
                    await Tcprooter().run(writer, malicious_ip, msg)
                else:
                    writer.close()
        return


"""
