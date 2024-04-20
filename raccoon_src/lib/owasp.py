from raccoon_src.generate_html import generate

class XSS:
    def __init__(self):
        pass

class LFI:
    def __init__(self):
        pass

class RFI:
    def __init__(self):
        pass

class Traversal:
    def __init__(self):
        pass

class RCE:
    def __init__(self):
        pass

class OWASPScanner:
    def __init__(self):
        self.running_threads = []
        # params
        pass

    def discover_xss(self):
        # if potentially vulnerable, create instance and run scan in a new thread
        pass

    def discover_lfi(self):
        # if potentially vulnerable, create instance and run scan in a new thread
        pass

    def discover_rfi(self):
        # if potentially vulnerable, create instance and run scan in a new thread
        pass

    def run(self):
        # Perform all checks, create relevant threads
        
        # Call the generate function after performing checks
        generate([])  # Pass any relevant information to generate the HTML output
