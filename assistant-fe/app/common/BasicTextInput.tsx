import {Input, Label, TextField} from "@heroui/react";


export function BasicTextInput() {
  return (
    <TextField className="w-full max-w-64" name="email" type="email">
      <Label>Query</Label>
      <Input placeholder="Type your query!" />
    </TextField>
  );
}