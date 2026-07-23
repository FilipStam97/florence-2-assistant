import cv2
import numpy as np
from pathlib import Path
from enum import Enum

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

    coords = data.get("quad_boxes") or data.get("bboxes")

    if coords is None:
        raise ValueError(f"No coordinates found. Keys: {list(data.keys())}")

    # Iterate through every detected OCR region and its corresponding text
    for box, label in zip(coords, labels):
        box_array = np.array(box, dtype=np.float32)

        # OCR_WITH_REGION returns 8 values:
        # [x1, y1, x2, y2, x3, y3, x4, y4]
        if box_array.size == 8:
            pts = box_array.reshape(4, 2)

        # Object detection and similar tasks return 4 values:
        # [x1, y1, x2, y2]
        elif box_array.size == 4:
            x1, y1, x2, y2 = box_array

            # Convert the rectangle into four corner points
            pts = np.array(
                [
                    [x1, y1],
                    [x2, y1],
                    [x2, y2],
                    [x1, y2],
                ],
                dtype=np.float32,
            )

        else:
            raise ValueError(
                f"Unsupported box format with {box_array.size} values: {box}"
            )

        pts = np.round(pts).astype(np.int32)

        cv2.polylines(
            image,
            [pts],
            isClosed=True,
            color=(0, 255, 0),
            thickness=2,
        )

        text_x = int(pts[:, 0].min())
        text_y = max(int(pts[:, 1].min()) - 5, 20)

        cv2.putText(
            image,
            label,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

    output_filename = save_image_return_filename(image, image_path)
    return output_filename



def draw_polygons(data: dict, image_path: Path) -> str:
    """
    Draw segmentation polygons and their labels on an image.

    Args:
        image: OpenCV image.
        polygons: List of polygons returned by Florence-2.
        labels: Corresponding labels.
    """

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

    polygons = data.get("polygons")

    if polygons is None:
        raise ValueError(f"No coordinates found. Keys: {list(data.keys())}")
    
    for polygon_group, label in zip(polygons, labels):
        # A single object may consist of multiple polygons
        for polygon in polygon_group:
            pts = np.array(polygon, dtype=np.float32).reshape(-1, 2)
            pts = np.round(pts).astype(np.int32)

            # Draw polygon outline
            cv2.polylines(
                image,
                [pts],
                isClosed=True,
                color=(0, 255, 0),
                thickness=2,
            )

            # Uncomment to fill the polygon instead
            # cv2.fillPoly(image, [pts], (0, 255, 0))

            # Draw the label near the top-left corner
            if label:
                text_x = int(pts[:, 0].min())
                text_y = max(int(pts[:, 1].min()) - 5, 20)

                cv2.putText(
                    image,
                    label,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2,
                )

    output_filename = save_image_return_filename(image, image_path)
    return output_filename

def save_image_return_filename(image, image_path: Path):
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


class Prompt(Enum):
    CAPTION = "<CAPTION>"
    DETAILED_CAPTION = "<DETAILED_CAPTION>"
    MORE_DETAILED_CAPTION = "<MORE_DETAILED_CAPTION>"
    OCR = "<OCR>"
    OCR_WITH_REGION = "<OCR_WITH_REGION>"
    OD = "<OD>"
    DENSE_REGION_CAPTION = "<DENSE_REGION_CAPTION>"
    REGION_PROPOSAL = "<REGION_PROPOSAL>"
    CAPTION_TO_PHRASE_GROUNDING = "<CAPTION_TO_PHRASE_GROUNDING>"
    REFERRING_EXPRESSION_SEGMENTATION = "<REFERRING_EXPRESSION_SEGMENTATION>"
    OPEN_VOCABULARY_DETECTION = "<OPEN_VOCABULARY_DETECTION>"
    REGION_TO_SEGMENTATION = "<REGION_TO_SEGMENTATION>"
    REGION_TO_CATEGORY = "<REGION_TO_CATEGORY>"
    REGION_TO_DESCRIPTION = "<REGION_TO_DESCRIPTION>"
    REGION_TO_OCR = "<REGION_TO_OCR>"