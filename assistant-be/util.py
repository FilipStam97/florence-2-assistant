import cv2
import numpy as np
from pathlib import Path
from enum import Enum

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"


def annotate_detection(data: dict, image_path: Path) -> str:

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Draw bounding or quadrilateral boxes when present
    if data.get("quad_boxes") or data.get("bboxes"):
        draw_boxes(image, data)

    # Draw segmentation polygons when present
    if data.get("polygons"):
        draw_polygons(image, data)

    return save_image_return_filename(image, image_path)

    
def draw_boxes(image: np.ndarray, data: dict) -> None:
    coords = data.get("quad_boxes") or data.get("bboxes")

    if not coords:
        return

    # Different Florence prompts use different label keys
    raw_labels = (
        data.get("labels")
        or data.get("bboxes_labels")
        or []
    )

    labels = [
        label.replace("</s>", "").strip()
        for label in raw_labels
    ]

    # Ensure every box has a label, even when Florence returns none
    labels.extend([""] * (len(coords) - len(labels)))

    for box, label in zip(coords, labels):
        box_array = np.array(box, dtype=np.float32)

        # Quadrilateral:
        # [x1, y1, x2, y2, x3, y3, x4, y4]
        if box_array.size == 8:
            pts = box_array.reshape(4, 2)

        # Rectangle:
        # [x1, y1, x2, y2]
        elif box_array.size == 4:
            x1, y1, x2, y2 = box_array

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
                f"Unsupported box format with "
                f"{box_array.size} values: {box}"
            )

        pts = np.round(pts).astype(np.int32)

        cv2.polylines(
            image,
            [pts],
            isClosed=True,
            color=(0, 255, 0),
            thickness=2,
        )

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



def draw_polygons(image: np.ndarray, data: dict) -> None:
    polygons = data.get("polygons")

    if not polygons:
        return

    raw_labels = (
        data.get("polygons_labels")
        or data.get("labels")
        or []
    )

    labels = [
        label.replace("</s>", "").strip()
        for label in raw_labels
    ]

    labels.extend([""] * (len(polygons) - len(labels)))

    for polygon_group, label in zip(polygons, labels):
        # One detected object may contain multiple separate polygons
        for polygon in polygon_group:
            polygon_array = np.array(polygon, dtype=np.float32)

            if polygon_array.size < 6 or polygon_array.size % 2 != 0:
                raise ValueError(
                    f"Invalid polygon with "
                    f"{polygon_array.size} coordinate values"
                )

            pts = polygon_array.reshape(-1, 2)
            pts = np.round(pts).astype(np.int32)

            cv2.polylines(
                image,
                [pts],
                isClosed=True,
                color=(0, 255, 0),
                thickness=2,
            )

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

def save_image_return_filename(
    image: np.ndarray,
    image_path: Path,
) -> str:
    outputs_dir = Path(BASE_DIR) / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    output_filename = f"result_{image_path.name}"
    output_path = outputs_dir / output_filename

    if not cv2.imwrite(str(output_path), image):
        raise RuntimeError(
            f"Could not save annotated image: {output_path}"
        )

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