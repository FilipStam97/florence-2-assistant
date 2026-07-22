import os
import cv2
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"


def annotate(image_path: str):
    image = cv2.imread(image_path)
    if(image != None):
        cv2.rectangle(image, (50, 50), (200, 200), (0, 255, 0), 3)
    
def annotate_ocr(data: dict, image_path: Path) -> str:
    # Load the image from disk using OpenCV
    image = cv2.imread(str(image_path))

    # Ensure the image was loaded successfully
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Remove Florence-2 special tokens (e.g. "</s>") from the OCR labels
    labels = [
        label.replace("</s>", "").strip()
        for label in data["labels"]
    ]

    # Iterate through every detected OCR region and its corresponding text
    for box, label in zip(data["quad_boxes"], labels):

        # Florence returns each quadrilateral as:
        # [x1, y1, x2, y2, x3, y3, x4, y4]
        # Reshape it into four (x, y) coordinate pairs.
        pts = np.array(box, dtype=np.float32).reshape(4, 2)

        # Convert floating-point coordinates into integer pixel coordinates
        # required by OpenCV drawing functions.
        pts = np.round(pts).astype(np.int32)

        # Draw the OCR quadrilateral using a green outline
        cv2.polylines(
            image,
            [pts],
            isClosed=True,
            color=(0, 255, 0),
            thickness=2,
        )

        # Position the label above the bounding box.
        # Using the minimum x/y values places it near the top-left corner.
        text_x = int(pts[:, 0].min())
        text_y = max(int(pts[:, 1].min()) - 5, 20)

        # Draw the recognized text in red
        cv2.putText(
            image,
            label,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

    # Create the output directory if it doesn't already exist
    outputs_dir = Path(BASE_DIR) / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Generate the output filename while preserving the original filename
    output_filename = f"result_{image_path.name}"
    output_path = outputs_dir / output_filename

    # Save the annotated image to disk
    if not cv2.imwrite(str(output_path), image):
        raise RuntimeError(f"Could not save annotated image: {output_path}")

    # Return the output filename so it can be sent back to the client
    return output_filename