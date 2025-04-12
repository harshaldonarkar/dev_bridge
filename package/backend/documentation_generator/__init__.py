from .gemini_generator import GeminiDocumentationGenerator

# Use the Gemini generator as the main documentation generator
DocumentationGenerator = GeminiDocumentationGenerator

__all__ = ['DocumentationGenerator']