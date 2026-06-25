import { Button } from "@heroui/react";
import Image from "next/image";
import PromptDropdown from "./common/PromptDropdown";
import { FLORENCE_2_PROMPTS } from "./constants";
import ImageDropZone from "./common/ImageDropZone";
import { BasicTextInput } from "./common/BasicTextInput";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center bg-black justify-center font-sans dark:bg-black">
      <main className="flex flex-1 w-full max-w-3xl items-center py-32 px-16 bg-white dark:bg-black sm:items-start">
        <div>
          <h1>Assistant</h1>
          <PromptDropdown prompts={FLORENCE_2_PROMPTS}/>
          <ImageDropZone />
          <BasicTextInput />
        </div>

      </main>
    </div>
  );
}
