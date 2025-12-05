import torch
import spacy
from transformers import BlipProcessor,BlipForConditionalGeneration
from PIL import Image
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_processor = None
_model = None
_nlp = None
en_stopwords = stopwords.words("english")

def load_models():
    global _processor, _model

    if _processor is None or _model is None:
        print("Loading models this may take sometime")

        _processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large", text="a detailed description")
        _model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(DEVICE)

        print("Models loaded successfully!")

    return _processor, _model

def generate_caption(image, min_length=50, max_length=200, num_beams=5, temperature=1.0):
    try:
        processor, model = load_models()

        # Open and process image
        img = Image.open(image).convert("RGB")

        # Generate caption
        inputs = processor(images=img, return_tensors="pt").to(DEVICE)
        out = model.generate(
            **inputs,
            min_length=min_length,
            max_length=max_length,
            num_beams=num_beams,
            temperature=temperature,
            top_k=50,
            repetition_penalty=1.5,  # ADD THIS - penalizes repetition
            no_repeat_ngram_size=3,  # ADD THIS - prevents 3-word phrases from repeating
            early_stopping=True
        )
        caption = processor.decode(out[0], skip_special_tokens=True)

        return caption

    except Exception as e:
        print(f"Error generating caption: {e}")
        return f"Error: Could not generate caption"

def extract_tags(caption, max_tags=6):
    global _nlp

    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")

    doc = _nlp(caption)
    tags = []

    for np in doc.noun_chunks:
        tag = np.text.lower().strip()
        if tag not in en_stopwords:
            tags.append(tag)
        if len(tags) > max_tags: break

    return tags

if __name__ == "__main__":
    import nltk
    from nltk.corpus import stopwords
    nltk.download("stopwords")
    en_stopwords = stopwords.words("english")
    print(en_stopwords)
