import { Prompt, PromptType } from "../constants";
import { CaptionDisplay } from "./CaptionDisplay";
import { ImageDisplay } from "./ImageDisplay";

const captionPrompts = new Set<Prompt>([
  Prompt.CAPTION,
  Prompt.DETAILED_CAPTION,
  Prompt.MORE_DETAILED_CAPTION,
  Prompt.OCR,
  Prompt.REGION_TO_CATEGORY,
  Prompt.REGION_TO_DESCRIPTION,
  Prompt.REGION_TO_OCR
]);

const imagePrompts = new Set<Prompt>([
  Prompt.OCR_WITH_REGION,
  Prompt.OD,
  Prompt.DENSE_REGION_CAPTION,
  Prompt.REGION_PROPOSAL,
  Prompt.CAPTION_TO_PHRASE_GROUNDING,
  Prompt.REFERRING_EXPRESSION_SEGMENTATION,
  Prompt.REGION_TO_SEGMENTATION,
  Prompt.OPEN_VOCABULARY_DETECTION,
]);


interface ResponseProps {
  prompt: {
    prompt: Prompt;
    promptName: string;
    promptType: PromptType;
  }
  data: any;
}


export const ResponseComponent: React.FC<ResponseProps> = ({ prompt, data }) => {

        if (captionPrompts.has(prompt.prompt)) {
            return (<CaptionDisplay title={prompt.promptName} text={data.caption}/>);
        }
        if (imagePrompts.has(prompt.prompt)) {
            return (<ImageDisplay title={prompt.promptName} src={data.imgSrc}/>);
        }

        return (<div>Unsupported layout type for data: {JSON.stringify(data)}</div>);
};