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

## The Harness (Drop-In Wrapper)

If you don't want to manually compress every prompt, you can use the built-in Harness to automatically wrap your LLM API calls.

### Option 1: Decorator
You can decorate any function that accepts `prompt` or `messages` (OpenAI format).

```python
from harness import minify_llm_args
import openai

client = openai.OpenAI()

@minify_llm_args
def generate_response(messages):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

# The messages will automatically be minified before hitting OpenAI!
response = generate_response([{"role": "user", "content": "Analyze this code: \n\n```python\n# test\ndef foo():\n    pass\n```"}])
```

### Option 2: Function Wrapper
Wrap an existing library call on the fly:

```python
from harness import call_with_minification

response = call_with_minification(
    client.chat.completions.create,
    model="gpt-4o",
    messages=[{"role": "user", "content": long_unoptimized_payload}]
)
```

## Setup
Simply drop `llm_minify.py` and `harness.py` into your project. You can manually pass strings through `compress_prompt(text)` or use the harness to automate it.
