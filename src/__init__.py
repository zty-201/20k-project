"""
Gemini RAG Agent package.
"""


from phoenix.otel import register                 # sets up a local OTLP collector
from openinference.instrumentation.langchain import LangChainInstrumentor

# 1) Create / configure a global tracer provider
tracer_provider = register()                      # default project = "default"

# 2) Instrument LangChain once
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)