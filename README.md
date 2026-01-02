# 🐱 Meowfacts API Integration

A robust Python client for the [Meowfacts API](https://meowfacts.herokuapp.com/) that automatically collects, deduplicates, and maintains a master dataset of cat facts across all supported languages.

---

## 📋 Overview

This integration is designed to build and maintain a **clean, analyst-ready dataset** of cat facts. It runs daily updates, dynamically discovers new languages, and ensures **zero duplicate entries** in the final output.

### Key Features

| Feature | Description |
|---------|-------------|
| 🌍 **Multi-language Support** | Automatically discovers and processes all languages supported by the API |
| 🔄 **Dynamic Discovery** | Adapts to API changes without manual updates |
| 🧹 **Deduplication** | Ensures a clean dataset with no duplicate facts |
| 💾 **Persistent Storage** | Maintains a master JSON file that grows over time |
| 🛡️ **Error Resilience** | Built-in retry logic and comprehensive error logging |

---

## 🏗️ How It Works

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  1. Discover     │────▶│  2. Fetch Facts  │────▶│  3. Deduplicate  │
│  Languages       │     │  (per language)  │     │  & Merge         │
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │                                                  │
         ▼                                                  ▼
┌──────────────────┐                              ┌──────────────────┐
│  /options        │                              │  Save to JSON    │
│  endpoint        │                              │  master file     │
└──────────────────┘                              └──────────────────┘
```

### Step-by-Step Process

1. **Language Discovery**  
   Queries the `/options` endpoint to retrieve all available ISO language codes and their respective fact counts.

2. **Cumulative Counting**  
   Intelligently sums fact counts for regional variants (e.g., `esp-es` and `esp-mx` are combined under `esp`), maximizing data retrieval efficiency.

3. **Data Fetching**  
   Requests the full pool of facts for each language in a single API call, with up to 5 retry attempts for transient failures.

4. **Deduplication**  
   Merges newly fetched facts with existing data using Python's `set` logic to eliminate duplicates.

5. **Persistence**  
   Saves the updated master dataset to a JSON file, preserving all historical data.

---

## 📦 Installation

### Prerequisites

- Python 3.7+
- `requests` library

### Setup

```bash
# Clone the repository
git clone https://github.com/roiegonen6/meowfacts_api
cd meowfacts_api
```

Then run:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Basic Execution

```bash
python meowfacts_api.py
```

### Expected Output

```
Found 12 unique ISO languages with cumulative counts.
Language   | Total Before    | New Unique Facts
-----------------------------------------------
eng        | 0               | 67
esp        | 0               | 45
ger        | 0               | 23
...

SUCCESS! Master dataset updated.
All discovered languages were processed successfully.
```

---

## 📁 Output Format

The script generates a `meowfacts_master_dataset.json` file with the following structure:

```json
{
    "eng": [
        "Cats have over 20 vocalizations, including the purr.",
        "A group of cats is called a clowder.",
        "Cats sleep for about 70% of their lives."
    ],
    "esp": [
        "Los gatos tienen más de 20 vocalizaciones.",
        "Un grupo de gatos se llama clowder."
    ],
    "ger": [
        "Katzen schlafen etwa 70% ihres Lebens."
    ]
}
```

Each language code maps to an array of **unique** cat facts.

---

## ⚙️ Configuration

The client can be customized by modifying the class attributes:

| Attribute | Default | Description |
|-----------|---------|-------------|
| `base_url` | `https://meowfacts.herokuapp.com/` | Main API endpoint |
| `options_url` | `https://meowfacts.herokuapp.com/options` | Metadata endpoint |
| `data_file` | `meowfacts_master_dataset.json` | Output file name |

---

## 🛡️ Error Handling

The integration includes robust error handling:

- **Network Failures**: Automatic retry up to 5 times per language
- **API Timeouts**: 10-second timeout with graceful fallback
- **Missing Languages**: Falls back to English (`eng`) if discovery fails
- **Error Summary**: All errors are collected and reported at execution end

Example error output:

```
--- Error Summary ---
Error fetching ISO code xyz: Connection timeout
```

---

## 🔌 API Reference

### Meowfacts API Capabilities

| Parameter | Description | Example |
|-----------|-------------|---------|
| `count` | Number of facts to retrieve | `?count=10` |
| `lang` | Language ISO code | `?lang=esp` |
| `id` | Specific fact ID | `?id=abc123` |

### Supported Languages

Languages are discovered dynamically. Common examples include:

- `eng` - English
- `esp` - Spanish
- `ger` - German
- `rus` - Russian
- `ukr` - Ukrainian
- `zho` - Chinese
- And more...

---

## 🗓️ Scheduling Daily Updates

### Linux/macOS (cron)

```bash
# Edit crontab
crontab -e

# Add daily execution at 8 AM
0 8 * * * /usr/bin/python3 /path/to/meowfacts_api.py
```

### Windows (Task Scheduler)

Create a scheduled task to run the Python script daily.

---

<p align="center">
  <i>Roie Gonen</i>
</p>

