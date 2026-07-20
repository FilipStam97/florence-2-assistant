"use client"
import {Label, ListBox, Select} from "@heroui/react";

type PromptDropdownProps = {
    prompts: Array<{prompt: string, promptName: string, promptType: string}>,
    prompt: string,
    setPrompt: any,
    resetMessage: Function
}

export default function PromptDropdown({prompts,prompt,setPrompt, resetMessage}: PromptDropdownProps) {


    const items = prompts.map(promptItem => (
          <ListBox.Item className="text-black" value={promptItem.prompt} id={promptItem.prompt} key={promptItem.prompt} textValue={promptItem.promptName}>
            {promptItem.promptName}
            <ListBox.ItemIndicator />
          </ListBox.Item>
    ))

   return (
    <Select className="w-[256px] py-4" placeholder="Select one" onChange={(value) => {
      console.log(value)
      resetMessage()
      setPrompt(value)
      }}  value={prompt}>
      <Label>Propmt</Label>
      <Select.Trigger>
        <Select.Value />
        <Select.Indicator />
      </Select.Trigger>
      <Select.Popover>
        <ListBox>
            {items}
         </ListBox>
    </Select.Popover>
    </Select>
  );

}