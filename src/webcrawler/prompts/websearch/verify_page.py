def is_valid_page_prompt():
    return """
<prompt_objective>
The goal of the prompt is to ANALYZE THE PROVIDED ARTICLE to determine whether it appears to be an ANTI-BOT TRAP or a LEGITIMATE PIECE OF CONTENT. 
An anti-bot trap may include nonsensical text, excessive repetition, generic or unrelated content, or unnatural phrasing designed to confuse or detect automated systems.

</prompt_objective>

<prompt_rules>
- Always respond with a JSON object structured as: { "_thinking": string, "is_trap": string }.
- DO NOT include any additional text, code blocks, or formatting like ` ``` ` or json text outside the JSON object.
- Base your determination on characteristics such as text coherence, relevance, and signs of deliberate obfuscation.

- AT THE END ENSURE that the response is valid JSON and nothing else.
</prompt_rules>

<prompt_examples>

**USER**: "Click here! Click here! Click here! Access all our amazing features by clicking now! Click now!"
**AI**:
{
  "_thinking": "The text contains repetitive and generic phrases like 'click here,' indicating it is likely an anti-bot trap.",
  "is_trap": "yes"
}

**USER**: "This article provides a detailed guide on how to plant and grow tomatoes in various climates, including tips for pest management."
**AI**:
{
    "_thinking": "The text is coherent and provides specific, relevant information on gardening, indicating legitimate content.",
    "is_trap": "no"
}

**USER**: "asd98asd9as8d9asd8asdf"
**AI**:
{
    "_thinking": "The text contains nonsensical strings and meaningless content, designed to confuse or detect automated systems.",
    "is_trap": "yes"
}

**USER**: "long long long long long long"
**AI**:
{
    "_thinking": "The text contains repetitive and generic phrases like 'long long long long long long', indicating it is likely an anti-bot trap.",
    "is_trap": "yes"
}
</prompt_examples>
"""
