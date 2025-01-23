from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import requests
import json
import os
from Utilities.configuration import get_setting_value
from Utilities.aux_io import get_settings_path
import re

class ProxyManager:
    def __init__(self):
        self.proxy_settings_path = get_settings_path(get_setting_value("proxy_settings", "PROXIES_PATH"))

    def get_list_of_proxies(self):
        scrapper = Scrapper(category='ALL', print_err_trace=False)
        data = scrapper.getProxies()
        return [f"{item.category}:{item.ip}:{item.port}" for item in data.proxies]

    def remove_candidate(self, candidates, candidate):
        """Remove a candidate from the list and update the file."""
        if candidate in candidates:
            candidates.remove(candidate)
            self.save_candidates(candidates)
            print(f"Removed candidate: {candidate}")
        else:
            print(f"Candidate not found: {candidate}")

    def save_candidates(self, candidates):
        """Save candidates to file."""
        with open(self.proxy_settings_path, 'w') as file:
            json.dump(candidates, file)

    import os
    import json
    import re

    def load_candidates(self):
        """Load candidates from file, return empty list if file doesn't exist or contains invalid content."""
        if os.path.exists(self.proxy_settings_path):
            with open(self.proxy_settings_path, 'r') as file:
                print("Loaded existing dump file with candidates:")
                try:
                    candidates = json.load(file)
                    if isinstance(candidates, list):
                        valid_ip_port_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$')
                        valid_candidates = [candidate for candidate in candidates if
                                            valid_ip_port_pattern.match(candidate)]
                        if valid_candidates:
                            return valid_candidates
                        else:
                            print("No valid IP;port entries found in the dump file. Starting fresh.")
                            return []
                    else:
                        print("Invalid JSON format. Starting fresh.")
                        return []
                except json.JSONDecodeError:
                    print("Error decoding JSON from file. Starting fresh.")
                    return []
        print("No existing dump file found. Starting fresh.")
        return []

    def get_proxies(self):
        return self.get_list_of_proxies(),self.load_candidates()


if __name__ == "__main__":


    proxy_manager = ProxyManager()
    candidates = proxy_manager.load_candidates()
    #proxy_manager.remove_candidate(candidates, 'candidate_to_remove')
    proxies = proxy_manager.get_list_of_proxies()
