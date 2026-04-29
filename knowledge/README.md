# Knowledge

Files dropped here become **shared context** for the crew via crewAI's
`TextFileKnowledgeSource` (and friends). Wiring lives in `crew.py`:

```python
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

Crew(
    ...,
    knowledge_sources=[TextFileKnowledgeSource(file_paths=["company_brief.txt"])],
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}},
)
```

`file_paths` is **relative to this directory**. Drop in PDFs, CSVs, JSON, or
arbitrary text — there's a knowledge source class for each. See
<https://docs.crewai.com/concepts/knowledge> for the full list.

`company_brief.txt` is a sample fictional company profile. Replace it with
your own context (product docs, style guides, policy snippets) before shipping.
