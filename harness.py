import functools
from llm_minify import compress_prompt

def minify_llm_args(func):
    """
    A decorator harness that automatically minifies 'prompt', 'messages', 
    or 'text' arguments passed to an LLM generation function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Check for standard 'prompt' kwarg
        if 'prompt' in kwargs and isinstance(kwargs['prompt'], str):
            kwargs['prompt'] = compress_prompt(kwargs['prompt'])
            
        # 2. Check for OpenAI-style 'messages' kwarg
        if 'messages' in kwargs and isinstance(kwargs['messages'], list):
            minified_messages = []
            for msg in kwargs['messages']:
                new_msg = dict(msg)
                if 'content' in new_msg and isinstance(new_msg['content'], str):
                    new_msg['content'] = compress_prompt(new_msg['content'])
                minified_messages.append(new_msg)
            kwargs['messages'] = minified_messages
            
        # 3. Check for Anthropic/general 'text' kwarg
        if 'text' in kwargs and isinstance(kwargs['text'], str):
            kwargs['text'] = compress_prompt(kwargs['text'])
            
        # Execute the original function with minified arguments
        return func(*args, **kwargs)
        
    return wrapper

class LLMMinifierHarness:
    """
    An object-oriented harness to wrap an entire LLM client instance.
    """
    def __init__(self, client):
        self._client = client
        
    def __getattr__(self, name):
        """
        Passes attribute access to the underlying client, wrapping callable methods.
        This is a simplistic approach and may need adaptation for deeply nested clients.
        """
        attr = getattr(self._client, name)
        if callable(attr):
            return minify_llm_args(attr)
        return attr

# Example standalone wrapper function if they just want to wrap a single call
def call_with_minification(llm_func, *args, **kwargs):
    """
    Pass the LLM function and its arguments here to execute it with minification.
    """
    @minify_llm_args
    def execute(*a, **kw):
        return llm_func(*a, **kw)
        
    return execute(*args, **kwargs)
