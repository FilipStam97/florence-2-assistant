"use client"
import {Label, ListBox, Select} from "@heroui/react";

type PromptDropdownProps = {
    prompts: Array<{prompt: string, promptName: string, promptType: string}>
}

export default function PromptDropdown({prompts}: PromptDropdownProps) {


    const items = prompts.map(prompt => (
          <ListBox.Item className="text-black" id={prompt.prompt} key={prompt.prompt} textValue={prompt.promptName}>
            {prompt.promptName}
            <ListBox.ItemIndicator />
          </ListBox.Item>
    ))

   return (
    <Select className="w-[256px]" placeholder="Select one">
      <Label>State</Label>
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