from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import cv2, re, torch, tempfile

# Load TrOCR model
def load_model():
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
    return processor, model

processor, model = load_model()

def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_file.name)
    image_cv = cv2.imread(temp_file.name)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(temp_file.name, thresh)
    return temp_file.name

def extract_text(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return text.strip()

def parse_item_info(ocr_text):
    item_match = re.search(r'(?i)([A-Za-z]+)', ocr_text)
    qty_match = re.search(r'(?i)(?:qty|quantity)\s*[:\- ]*\s*(\d+)', ocr_text)
    price_match = re.search(r'(?i)(?:price|₹|\$)\s*[:\- ]*\s*([\d\.]+)', ocr_text)
    item_name = item_match.group(1).title() if item_match else None
    quantity = int(qty_match.group(1)) if qty_match else None
    price = float(price_match.group(1)) if price_match else None
    if quantity is not None:
        quantity =float(f"{quantity:.2f}")
    if price is not None:
        price = float(f"{price:.2f}")
    return item_name, quantity, price
