"""Application boundaries: optional adapters, atomic startup, and a usable offline UI."""

from contextlib import redirect_stdout
import gc
import io
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import Mock, patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import main
from session import SessionClosed


class ApplicationTests(unittest.TestCase):
    def fake_services(self, events, failure=None):
        modules = {}
        instances = {}
        for name, module, class_name in main.SERVICE_TYPES:
            def factory(protocol, host, port, *, log, name=name):
                service = Mock()
                service.port = port
                service.running = False
                service.error = None

                def bind():
                    events.append("bind " + name)
                    if failure == (name, "bind"):
                        raise OSError("address already in use")

                def start():
                    events.append("start " + name)
                    if failure == (name, "start"):
                        raise RuntimeError("worker failed")
                    service.running = True

                def close():
                    events.append("close " + name)
                    service.running = False

                service.bind.side_effect = bind
                service.start.side_effect = start
                service.close.side_effect = close
                service.status.side_effect = lambda: {
                    "running": service.running, "error": service.error,
                    "port": port, "clients": 0}
                instances[name] = service
                return service
            modules[module] = types.SimpleNamespace(**{class_name: factory})
        return modules, instances

    def test_partial_bind_failure_closes_all_and_never_starts(self):
        events = []
        modules, instances = self.fake_services(events, failure=("udp", "bind"))
        app = main.Application(main.parse_args(["--no-window"]))
        with patch.dict(sys.modules, modules), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "UDP.*8267"):
                app.start()
            app.close()
        self.assertEqual(events, ["bind tcp", "bind udp", "close http", "close udp", "close tcp"])
        for service in instances.values():
            service.close.assert_called_once()
            service.start.assert_not_called()
        with self.assertRaises(SessionClosed):
            app.session.press_input()

    def test_partial_start_failure_rolls_back_in_reverse_order(self):
        events = []
        modules, _ = self.fake_services(events, failure=("udp", "start"))
        app = main.Application(main.parse_args(["--no-window"]))
        with patch.dict(sys.modules, modules), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "UDP.*8267"):
                app.start()
        self.assertEqual(events, ["bind tcp", "bind udp", "bind http", "start tcp", "start udp",
                                  "close http", "close udp", "close tcp"])

    def test_window_is_validated_before_binding_and_shown_after_start(self):
        events = []
        modules, _ = self.fake_services(events)
        root, window = Mock(), Mock()
        root.withdraw.side_effect = lambda: events.append("withdraw")
        root.deiconify.side_effect = lambda: events.append("show")
        root.destroy.side_effect = lambda: events.append("destroy")
        modules["tkinter"] = types.SimpleNamespace(Tk=lambda: root)
        app = main.Application(main.parse_args([]))
        with patch.dict(sys.modules, modules), patch.object(main, "Window", return_value=window), \
                redirect_stdout(io.StringIO()):
            try:
                app.start()
                self.assertEqual(events[:7], ["withdraw", "bind tcp", "bind udp", "bind http",
                                               "start tcp", "start udp", "start http"])
                self.assertEqual(events[-1], "show")
            finally:
                app.close()
        window.close.assert_called_once()
        self.assertEqual(events[-1], "destroy")

    def test_window_failure_never_constructs_or_binds_services(self):
        events = []
        modules, instances = self.fake_services(events)
        modules["tkinter"] = types.SimpleNamespace(Tk=Mock(side_effect=RuntimeError("no display")))
        app = main.Application(main.parse_args([]))
        with patch.dict(sys.modules, modules), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "no display"):
                app.start()
        self.assertEqual(instances, {})
        self.assertEqual(events, [])

    def test_background_failure_is_reported_and_stops_application(self):
        events = []
        modules, instances = self.fake_services(events)
        app = main.Application(main.parse_args(["--no-window"]))
        with patch.dict(sys.modules, modules), redirect_stdout(io.StringIO()):
            try:
                app.start()
                instances["udp"].running = False
                instances["udp"].error = "listener failed"
                self.assertFalse(app.check_health())
                self.assertTrue(app.stop_event.is_set())
                self.assertEqual(app.exit_code, 1)
                self.assertIn("listener failed", app.runtime_state()["log"][-1])
            finally:
                app.close()

    def test_log_keeps_recent_twenty_entries(self):
        app = main.Application(main.parse_args(["--no-window"]))
        with redirect_stdout(io.StringIO()):
            for index in range(25):
                app.log(str(index))
        self.assertEqual(len(app.runtime_state()["log"]), 20)
        self.assertTrue(app.runtime_state()["log"][0].endswith(" 5"))
        app.close()

    def test_offline_native_window_changes_session_and_displays_exact_sensor_values(self):
        try:
            import tkinter as tk
        except ImportError:
            self.skipTest("Python does not include Tkinter")
        try:
            probe = tk.Tk()
            probe.withdraw()
            probe.update_idletasks()
            probe.destroy()
        except tk.TclError as error:
            self.skipTest("Tk display unavailable: %s" % error)
        # Release Tk objects on the main thread before later tests start network workers.
        self.addCleanup(gc.collect)
        app = main.Application(main.parse_args(["--no-tcp", "--no-udp", "--no-http"]))
        with redirect_stdout(io.StringIO()), patch.dict(sys.modules, {"tcp": None, "udp": None, "http_api": None}):
            try:
                app.start()
                app.root.withdraw()
                self.assertEqual(app.services, {})
                app.window.input_button.invoke()
                self.assertEqual(app.session.snapshot().state.input_value, 1)
                self.assertIn("1", app.window.input_button.cget("text"))
                app.window.slide("temperature", "32.75")
                self.assertEqual(app.session.snapshot().state.temperature, 32.8)
                app.session.set_environment(temperature=123.125, humidity=-2.25)
                app.window.refresh()
                self.assertEqual(app.window.sensor_values["temperature"][0].get(), 123.125)
                self.assertEqual(app.window.sensor_values["humidity"][0].get(), -2.25)
                self.assertNotIn("10.0.2.2", app.window.instructions.cget("text"))
                app.window.reset()
                self.assertEqual(app.session.snapshot().state.input_value, 0)
                app.root.update_idletasks()
            finally:
                app.close()
        self.assertIsNone(app.window.timer)


class CommandLineTests(unittest.TestCase):
    def run_python(self, *args, cwd=HERE):
        return subprocess.run([sys.executable, "-S", "-B", *args], cwd=cwd,
                              capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)

    def test_help_and_invalid_arguments(self):
        result = self.run_python("main.py", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for switch in ("--no-tcp", "--no-udp", "--no-http", "--no-window"):
            self.assertIn(switch, result.stdout)
        for arguments in (("--tcp", "-1"), ("--udp", "65536"), ("--http", "wrong"),
                          ("--name", " "), ("--no-window", "--no-tcp", "--no-udp", "--no-http")):
            with self.subTest(arguments=arguments):
                result = self.run_python("main.py", *arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_headless_http_mutation_never_imports_tk_or_tcp_or_udp(self):
        source = '''
import json, sys
from importlib import import_module
from urllib.request import Request, urlopen
sys.modules.update(tkinter=None, tcp=None, udp=None)
module = import_module(sys.argv[1])
app = module.Application(module.parse_args(["--no-window", "--no-tcp", "--no-udp", "--http", "0"]))
try:
    app.start()
    url = "http://127.0.0.1:%s" % app.services["http"].port
    with urlopen(Request(url + "/input", data=b"{}", method="POST"), timeout=2) as response:
        assert response.status == 200
    assert app.session.snapshot().state.input_value == 1
    assert app.discovery()["tcp"] is None
    assert sys.modules["tkinter"] is None and sys.modules["tcp"] is None and sys.modules["udp"] is None
finally:
    app.close()
'''
        for name, directory in (("main", HERE), ("wleno.main", HERE.parent)):
            with self.subTest(module=name):
                result = self.run_python("-c", source, name, cwd=directory)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
