# LLM Context Minifier 🚀

Save up to 40% on API costs (OpenAI, Anthropic, etc.) by mathematically minifying code and JSON blocks inside your LLM prompts, *without* losing logic or data.

Because LLMs are mathematical models, they can read minified JSON and flattened code blocks perfectly. You don't need formatting whitespace in your prompts!

## What it does
* **JSON**: Parses massive JSON outputs and minifies them `{"like":["this"]}`.
* **Python**: Strips docstrings, removes inline comments (`#`), and collapses blank lines.
* **JavaScript / CSS**: Rips out all `//` and `/* */` comments, flattening code blocks to a single line where structurally safe.
* **HTML**: Strips `<!-- -->` comments and snaps tags together (`><`) to eliminate indentation token bloat.
* **Fluff**: Removes conversational fluff from previous messages (e.g. "Here is the information you requested:").

## Simple Example

### Before Minification (High Token Cost)
```python
sample_payload = """
Here is the information you requested:

```json
{
    "nodes": [
        {
            "id": 1,
            "label": "Deep Context",
            "weight": 0.95
        }
    ]
}
```

```javascript
// Sample script
function test() {
    /* Multi
       line */
    console.log("testing");
}
```
"""
```

### Usage
```python
from llm_minify import compress_prompt

minified_payload = compress_prompt(sample_payload)
print(minified_payload)
```

### After Minification (Low Token Cost)
```
```json
{"nodes":[{"id":1,"label":"Deep Context","weight":0.95}]}
```

```javascript
function test() { console.log("testing"); }
```
```

## Setup
Simply drop `llm_minify.py` into your project and pass your string payloads through `compress_prompt(text)` before sending them to the LLM API.
