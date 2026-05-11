"""
Multi-language support for Alexandria
"""
import google.generativeai as genai
import os

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi"
}


async def translate_content(content: str, target_language: str) -> str:
    """
    Translate content to target language using Gemini
    
    Args:
        content: Text to translate
        target_language: Target language code (e.g., 'es', 'fr')
    
    Returns:
        Translated content
    """
    if target_language == "en":
        return content
    
    if target_language not in SUPPORTED_LANGUAGES:
        return content
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        target_lang_name = SUPPORTED_LANGUAGES[target_language]
        
        prompt = f"""Translate the following text to {target_lang_name}. 
Keep the meaning and context intact. Only return the translated text, nothing else.

Text to translate:
{content}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Translation error: {e}")
        return content


async def generate_summary_in_language(summary: str, language: str) -> str:
    """
    Generate or translate a summary to the specified language
    
    Args:
        summary: The summary text
        language: Target language code
    
    Returns:
        Summary in target language
    """
    return await translate_content(summary, language)


def get_language_name(language_code: str) -> str:
    """Get full language name from code"""
    return SUPPORTED_LANGUAGES.get(language_code, "English")


def validate_language_code(language_code: str) -> bool:
    """Validate if language code is supported"""
    return language_code in SUPPORTED_LANGUAGES
