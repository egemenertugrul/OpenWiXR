import subprocess
import logging
import multiprocessing as mp
from typing import Union
import psutil
import time


class ProcessHelper:
    @staticmethod
    def kill_processes_by_name(name: str):
        for process in psutil.process_iter(["pid", "name", "cmdline"]):
            if name in process.info["name"]:
                process.kill()

    @staticmethod
    def _log_subprocess_output(pipe):
        for line in iter(pipe.readline, b""):  # b'\n'-separated lines
            logging.info("SHELL: %r", line)

    @staticmethod
    def _kill(proc_pid):
        try:
            process = psutil.Process(proc_pid)
        except psutil.NoSuchProcess as e:
            logging.info(e)
            return
        else:
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()

    @staticmethod
    def _launch_command(command: str):
        exitcode = -1
        while exitcode != 0:
            _process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            with _process.stdout:
                ProcessHelper._log_subprocess_output(_process.stdout)
            exitcode = _process.wait()  # 0 means success

    @staticmethod
    def start_persistent_command_process(command: str) -> mp.Process:
        cmd_process = mp.Process(
            target=ProcessHelper._launch_command,
            args=(command,),
        )
        cmd_process.start()
        return cmd_process

    @staticmethod
    def start_process(executable_full_filepath, wd=None, args=None) -> subprocess.Popen:
        args = [str(arg) for arg in args if arg]
        command = [executable_full_filepath] + args
        process = subprocess.Popen(command, cwd=wd)
        return process

    @staticmethod
    def stop_process(process: Union[mp.Process, subprocess.Popen]):
        if isinstance(process, subprocess.Popen):
            process.terminate()
            process.wait()
        elif isinstance(process, mp.Process):
            ProcessHelper._kill(process.pid)
            process.join()