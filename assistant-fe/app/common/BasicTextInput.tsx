import {Input, Label, TextField} from "@heroui/react";


export function BasicTextInput({setInput, input}: {setInput: any, input: string}) {
  return (
    <TextField  className="w-full max-w-64 py-4" value={input} onChange={setInput}>
      <Label>Query</Label>
      <Input  placeholder="Type your query!" />
    </TextField>
  );
}