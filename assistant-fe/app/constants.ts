export const FLORENCE_2_PROMPTS: Array<{prompt: string, promptName: string, promptType: PromptType}> =   [
  {
    prompt: "<CAPTION>",
    promptName: "Caption",
    promptType: "caption",
  },
  {
    prompt: "<DETAILED_CAPTION>",
    promptName: "Detailed Caption",
    promptType: "caption",
  },
  {
    prompt: "<MORE_DETAILED_CAPTION>",
    promptName: "More Detailed Caption",
    promptType: "caption",
  },
  {
    prompt: "<OCR>",
    promptName: "OCR",
    promptType: "ocr",
  },
  {
    prompt: "<OCR_WITH_REGION>",
    promptName: "OCR with Region",
    promptType: "ocr",
  },
  {
    prompt: "<OD>",
    promptName: "Object Detection",
    promptType: "detection",
  },
  {
    prompt: "<DENSE_REGION_CAPTION>",
    promptName: "Dense Region Caption",
    promptType: "region-caption",
  },
  {
    prompt: "<REGION_PROPOSAL>",
    promptName: "Region Proposal",
    promptType: "proposal",
  },
  {
    prompt: "<CAPTION_TO_PHRASE_GROUNDING>",
    promptName: "Caption to Phrase Grounding",
    promptType: "grounding",
  },
  {
    prompt: "<REFERRING_EXPRESSION_SEGMENTATION>",
    promptName: "Referring Expression Segmentation",
    promptType: "segmentation",
  },
  {
    prompt: "<OPEN_VOCABULARY_DETECTION>",
    promptName: "Open Vocabulary Detection",
    promptType: "detection",
  },
  {
    prompt: "<REGION_TO_SEGMENTATION>",
    promptName: "Region to Segmentation",
    promptType: "segmentation",
  },
  {
    prompt: "<REGION_TO_CATEGORY>",
    promptName: "Region to Category",
    promptType: "classification",
  },
  {
    prompt: "<REGION_TO_DESCRIPTION>",
    promptName: "Region to Description",
    promptType: "caption",
  },
  {
    prompt: "<REGION_TO_OCR>",
    promptName: "Region to OCR",
    promptType: "ocr",
  }
];


export const PROMPTS_REQUIRING_TEXT_INPUT = [
  "<CAPTION_TO_PHRASE_GROUNDING>", "<REFERRING_EXPRESSION_SEGMENTATION>", "<OPEN_VOCABULARY_DETECTION>", "<REGION_TO_SEGMENTATION>"
]

export type PromptType =   "ocr" | "caption" |  "classification" |  "segmentation" |   "detection" |   "grounding" |   "proposal" |  "region-caption"


//4 caption, 3 ocr, 2 detection, 1 region-caption, 1 proposal, 1 grounding, 2 segmentation, 1 classification

export enum Prompt {
  CAPTION = "<CAPTION>",
  DETAILED_CAPTION = "<DETAILED_CAPTION>",
  MORE_DETAILED_CAPTION = "<MORE_DETAILED_CAPTION>",
  OCR = "<OCR>",
  OCR_WITH_REGION = "<OCR_WITH_REGION>",
  OD = "<OD>",
  DENSE_REGION_CAPTION = "<DENSE_REGION_CAPTION>",
  REGION_PROPOSAL = "<REGION_PROPOSAL>",
  CAPTION_TO_PHRASE_GROUNDING = "<CAPTION_TO_PHRASE_GROUNDING>",
  REFERRING_EXPRESSION_SEGMENTATION = "<REFERRING_EXPRESSION_SEGMENTATION>",
  OPEN_VOCABULARY_DETECTION = "<OPEN_VOCABULARY_DETECTION>",
  REGION_TO_SEGMENTATION = "<REGION_TO_SEGMENTATION>",
  REGION_TO_CATEGORY = "<REGION_TO_CATEGORY>",
  REGION_TO_DESCRIPTION = "<REGION_TO_DESCRIPTION>",
  REGION_TO_OCR = "<REGION_TO_OCR>",
}
