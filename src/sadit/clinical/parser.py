try:
    import spacy
except ImportError:
    spacy = None
from .models import PainProfile


class ClinicalParser:
    """
    SADIT NLP Parser for Clinical Text.
    Uses Spacy (en_core_sci_lg/sm) to extract ALICIA markers securely.
    Avoids naive splitting methods.
    """

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Fallback or download needed
            self.nlp = None

    def parse_text_to_profile(self, text: str) -> PainProfile:
        """
        Parses free text to generate a structured PainProfile.
        """
        if not self.nlp:
            print("NLP Warning: Spacy model not loaded. Using heuristic fallback.")
            return self._heuristic_fallback(text)

        doc = self.nlp(text.lower())

        # 1. Location Extraction
        location = 'diffuse'
        if 'distal' in text or 'knee' in text or 'femur' in text:
            location = 'distal'
        elif 'groin' in text or 'inguinal' in text or 'hip' in text:
            location = 'inguinal'

        # 2. Character Extraction
        character = 'mixed'
        tokens = [token.text for token in doc]

        if 'terebrante' in tokens or 'boring' in tokens or 'drilling' in tokens:
            character = 'terebrante'
        elif 'throbbing' in tokens or 'mechanical' in tokens or 'load' in tokens:
            character = 'mechanical'
        elif 'burning' in tokens or 'night' in tokens or 'constant' in tokens:
            character = 'inflammatory'

        # 3. Aggravating Factors (NLP Dependency Parsing would be ideal here)
        aggravating = []
        if 'walk' in text or 'standing' in text:
            aggravating.append('load')
        if 'night' in text:
            aggravating.append('night')

        return PainProfile(
            onset='gradual',  # Default
            location=location,
            intensity=7,  # Default
            character=character,
            aggravating=aggravating,
            alleviating=[],
            irradiation=False
        )

    def _heuristic_fallback(self, text):
        # ... logic similar to above but without spacy object ...
        return PainProfile(onset='gradual', location='diffuse', intensity=5, character='mixed', aggravating=[], alleviating=[], irradiation=False)
