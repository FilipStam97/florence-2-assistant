'use client'

import { Button, Card, Separator } from "@heroui/react";
import Image from "next/image";
import PromptDropdown from "./common/PromptDropdown";
import { FLORENCE_2_PROMPTS, PROMPTS_REQUIRING_TEXT_INPUT } from "./constants";
import ImageDropZone from "./common/ImageDropZone";
import { BasicTextInput } from "./common/BasicTextInput";
import { useState } from "react";
import { ResponseComponent } from "./common/ResponseComponent";

export default function Home() {
 const [image, setImage] = useState<File | null>(null);
  const [prompt, setPrompt] = useState('');
  const [textInput, setTextInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<any | undefined>(undefined);


  const displayTextInput = PROMPTS_REQUIRING_TEXT_INPUT.includes(prompt);

  const currentPrompt = FLORENCE_2_PROMPTS.find(pr => prompt === pr.prompt);

  const handleSubmit = async () => {
  
      if (!image) {
        alert('Please select an image file first.');
        return;
      }

      setLoading(true);
      setMessage('');


      const formData = new FormData();

      formData.append('image', image);
      formData.append('prompt', prompt);
      if(displayTextInput) {
          formData.append('text_input', textInput);
      }
      

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData, // Do NOT set 'Content-Type' header; the browser sets it automatically with the boundary line
      });

      const data = await response.json();
    
      if (response.ok) {
        setMessage(data);
      } else {
        setMessage(`Error`);
      }
      } catch (error) {
        console.error('Upload error:', error);
        setMessage('Network error occurred.');
      } finally {
        setLoading(false);
      }
    };

    function resetMessage() {
      setMessage(undefined);
    }



  return (
    <div className="flex flex-col flex-1 items-center bg-black justify-center font-sans dark:bg-black">
      <main className="flex flex-1 w-full max-w-3xl items-center py-10 px-16 bg-white dark:bg-black sm:items-start">
        <div>
          <h1 className="py-2 text-3xl">Florence-2 Vision-Language Assistant</h1>
          <PromptDropdown prompts={FLORENCE_2_PROMPTS} prompt={prompt} setPrompt={setPrompt} resetMessage={resetMessage} />
          <ImageDropZone  setImage={setImage} image={image}/>
          {displayTextInput && 
            <BasicTextInput setInput={setTextInput} input={textInput}/>
          }
          <div className="py-6">
            <Button isDisabled={loading} onClick={handleSubmit}>
              {loading ? 'Uploading...' : 'Upload Data'}
            </Button>
          </div>
          <div>
            {!loading && currentPrompt && message &&
              <ResponseComponent prompt={currentPrompt as any} data={message}/>
            }
      
          </div>
        </div>
      </main>
    </div>
  );
}
