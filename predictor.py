import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM 




class Florence2Model:
    def __init__(self) -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_id = "microsoft/Florence-2-base-ft"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id, torch_dtype=self.torch_dtype, trust_remote_code=True,attn_implementation="eager").to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_id,trust_remote_code=True)

#type this properly
    def run(self,image, task_prompt: str, text_input=None):
        if text_input is None:
            prompt = task_prompt
        else:
            prompt = task_prompt + text_input
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torch_dtype)
        generated_ids = self.model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3
        )
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

        parsed_answer = self.processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))

        print(parsed_answer)
        return parsed_answer
    


    

