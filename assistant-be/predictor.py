import os
from typing import Any
from unittest.mock import patch

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
from transformers.dynamic_module_utils import get_imports


def fixed_get_imports(filename: str | os.PathLike[str]) -> list[str]:
    imports = get_imports(filename)

    if str(filename).endswith("modeling_florence2.py"):
        imports = [package for package in imports if package != "flash_attn"]

    return imports


class Florence2Model:
    def __init__(self) -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.torch_dtype = (
            torch.float16
            if torch.cuda.is_available()
            else torch.float32
        )

        self.model_id = "microsoft/Florence-2-base-ft"

        with patch(
            "transformers.dynamic_module_utils.get_imports",
            fixed_get_imports,
        ):
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=self.torch_dtype,
                trust_remote_code=True,
                attn_implementation="eager",
            ).to(self.device)

        self.processor = AutoProcessor.from_pretrained(
            self.model_id,
            trust_remote_code=True,
        )

    def run(
        self,
        image: Image.Image,
        task_prompt: str,
        text_input: str | None = None,
    ) -> dict[str, Any]:
        prompt = (
            task_prompt
            if text_input is None
            else task_prompt + text_input
        )

        inputs = self.processor(
            text=prompt,
            images=image,
            return_tensors="pt",
        )

        # Move integer tensors without converting them to float.
        input_ids = inputs["input_ids"].to(self.device)

        pixel_values = inputs["pixel_values"].to(
            device=self.device,
            dtype=self.torch_dtype,
        )

        generated_ids = self.model.generate(
            input_ids=input_ids,
            pixel_values=pixel_values,
            max_new_tokens=1024,
            num_beams=3,
        )

        generated_text = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=False,
        )[0]

        return self.processor.post_process_generation(
            generated_text,
            task=task_prompt,
            image_size=(image.width, image.height),
        )