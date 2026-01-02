import requests
import json
import time
import os

class MeowFactsClient:
    def __init__(self):
        self.base_url = "https://meowfacts.herokuapp.com/"
        self.options_url = "https://meowfacts.herokuapp.com/options" #The /options endpoint provides the 'metadata' of the API
        self.data_file = "meowfacts_master_dataset.json"
        self.languages_info = {} #Store {iso_code: fact_count}
        self.errors = []

    def discover_languages(self): #Fetches ISO codes and sums fact counts dynamically from the API
        try:
            response = requests.get(self.options_url, timeout=10)
            response.raise_for_status()
            
            options_data = response.json().get("lang", [])
            for entry in options_data:
                iso = entry.get("iso_code")
                count = entry.get("fact_count", 1000) #Default to 1000 if missing 
                
                if iso in self.languages_info:
                    self.languages_info[iso] += count #Cumulative logic: If ISO exists, add the new count to the existing value
                else:
                    self.languages_info[iso] = count
            
            print(f"Found {len(self.languages_info)} unique ISO languages with cumulative counts.")
        except requests.exceptions.RequestException as e:
            self.errors.append(f"Critical Error: Could not discover languages via {self.options_url}: {e}")
            self.languages_info = {"eng": 1000}

    def load_existing_data(self):
        if os.path.exists(self.data_file): #Loads existing facts from the JSON file to prevent duplicates
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def fetch_facts(self, lang, fact_count, iterations=5): #Fetches facts using the fact_count ##Iterations set as 5 incase it failes and there is a need to re-try
        all_fetched_for_lang = []
        for i in range(iterations):
            params = {"lang": lang, "count": fact_count}
            try:
                time.sleep(0.2) 
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                
                batch = response.json().get("data", []) 
                # batch = ['test'] #For QA usage
                
                if not batch or batch == [None]:
                    break
                
                all_fetched_for_lang.extend(batch)
                break #Success break: if data was inserted successfully, stop further iterations for this languages
                
            except requests.exceptions.RequestException as e:
                self.errors.append(f"Error fetching ISO code {lang}: {e}")
        return all_fetched_for_lang

    def run_daily_update(self): #Main entry point to update the analyst dataset
        self.discover_languages()
        master_dataset = self.load_existing_data()
        
        print(f"{'Language':<10} | {'Total Before':<15} | {'New Unique Facts':<15}")
        print("-" * 47)

        for lang, fact_count in self.languages_info.items():
            if lang not in master_dataset:
                master_dataset[lang] = [] #Insert new languages if API was updated
                
            existing_facts = master_dataset.get(lang, [])
            count_before = len(existing_facts)
            
            new_raw_data = self.fetch_facts(lang, fact_count)
            
            updated_unique_list = list(set(existing_facts + new_raw_data)) #Combine new and current list and remove dups
            
            count_after = len(updated_unique_list)
            new_rows_added = count_after - count_before
            
            master_dataset[lang] = updated_unique_list
            print(f"{lang:<10} | {count_before:<15} | {new_rows_added:<15}")

        self.save_files(master_dataset)
        
        if self.errors:
            print("\n--- Error Summary ---")
            for error in set(self.errors):
                print(error)
        else:
            print("\nAll discovered languages were processed successfully.")

    def save_files(self, data): #Outputs a .json file with relevant data
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"\nSUCCESS! Master dataset updated.")
        except IOError as e:
            print(f"  -> File Error: {e}")

if __name__ == "__main__":
    client = MeowFactsClient()
    client.run_daily_update()