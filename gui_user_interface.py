"""Simple Async / Await / Thread Demo"""

# System Imports
import asyncio
import threading
import time

# Third Party Imports
import FreeSimpleGUI as sg 

class SyncAsyncAwaitDemoWindow:
    """Sync Async Await Demo Window"""

    def __init__(self):
        """Constructor"""

        self.progress = 0
        self.start = 0
        self.end = 0

        layout = [
            [sg.Text("Not Fetched Yet!", key ="-output-")],
            [sg.Text("0.00 seconds", key="-time_output-")],
            [
                sg.ProgressBar(
                    100,
                    orientation="h",
                    expand_x=True,
                    size=(20, 20),
                    key="-progress-",
                )
            ],
            [sg.Button("Submit Sync", key="-submit_sync-")],
            [sg.Button("Submit Async", key="-submit_async-")],
            [sg.Button("Submit Thread", key="-submit_thread-")],
            [sg.Button("Submit Thread Async", key="-submit_thread_async-")],
            [sg.Button("Submit Long Run", key="-submit_long_run-")],
            [sg.Button("Exit")],
        ]

        self.window = sg.Window("Async Await Thread Window", layout)

    def run(self):
        """Start the window"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the event loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "-submit_sync-":
                self._on_submit_sync(event, values)
            elif event == "-submit_async-":
                self._on_submit_async(event, values)
            elif event == "-submit_thread-":
                self._on_submit_thread(event, values)
            elif event == "-submit_thread_async-":
                self._on_submit_thread_async(event, values)
            elif event == "-submit_long_run-":
                self._on_submit_long_run(event, values)
            elif event == "-done_long_run-":
                self.end = time.time()
                elapsed = f"{(self.end - self.start):.2f} seconds"
                self.window["-output-"].update(values[event])
                self.window["-time_output-"].update(elapsed)

    def _on_submit_sync(self, event, values):
        """On submit sync"""
        start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name")
        self.window["-time_output-"].update("Calculating...")
        name = self._get_name()
        end = time.time()
        elapsed = f"{(end - start):.2f} seconds"
        self.window["-output-"].update(name)
        self.window["-time_output-"].update(elapsed)


    def _on_submit_async(self, event, values):
        """On submit async"""
        start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name")
        self.window["-time_output-"].update("Calculating...")
        name = asyncio.run(self._get_name_async())
        end = time.time()
        elapsed = f"{(end - start):.2f} seconds"
        self.window["-output-"].update(name)
        self.window["-time_output-"].update(elapsed)

    def _on_submit_thread(self, event, values):
        """On submit thread"""
        self.start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Threaded")
        self.window["-time_output-"].update("Calculating...")
        task = threading.Thread(
            target=self._get_name_thread,
            args=(), # For method above
        )
        task.start() # Makes thread

    def _on_submit_thread_async(self, event, values):
        """On submit thread async"""
        self.start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Threaded and Async")
        self.window["-time_output-"].update("Calculating...")
        task = threading.Thread(
            target=self._get_name_thread_and_async,
            args=(), # For method above
        )
        task.start() # Makes thread

    def _on_submit_long_run(self, event, values):
        """On submit long run"""
        self.start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Long Running")
        self.window["-time_output-"].update("Calculating...")
        self.window.perform_long_operation(self._get_name, "-done_long_run-")


    # The simulated long-running task methods are below.
    def _get_name(self):
        """Get name from long running task"""
        first = self._get_first_name()
        last = self._get_last_name()
        return f"{first} {last}"
    
    def _get_first_name(self):
        """Get first name from long running task"""
        for i in range(0, 10):
            time.sleep(0.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "David"
    
    def _get_last_name(self):
        """Get last name from long running task"""
        for i in range(0, 10):
            time.sleep(0.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "Barnes"
    
    async def _get_name_async(self):
        """Get the name asynchronously"""
        results = await asyncio.gather(
            self._get_first_name_async(),
            self._get_last_name_async(),
        )
        return f"{results[0]} {results[1]}"
    
    async def _get_first_name_async(self):
        """Get first name from long running task"""
        for i in range(0, 10):
            await asyncio.sleep(0.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "David"
    
    async def _get_last_name_async(self):
        """Get last name from long running task"""
        for i in range(0, 10):
            await asyncio.sleep(0.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "Barnes"
    
    def _get_name_thread(self):
        """Get name from long running task using a separate thread from the UI thread."""
        first = self._get_first_name()
        last = self._get_last_name()
        self.end = time.time()
        elapsed = f"{(self.end - self.start):.2f} seconds"
        self.window["-output-"].update(f"{first} {last}")
        self.window["-time_output-"].update(elapsed)

    def _get_name_thread_and_async(self):
        """Get name from long running task using a separate thread from the UI thread.
        And also using asyncio."""
        name = asyncio.run(self._get_name_async())
        self.end = time.time()
        elapsed = f"{(self.end - self.start):.2f} seconds"
        self.window["-output-"].update(f"{name}")
        self.window["-time_output-"].update(elapsed)