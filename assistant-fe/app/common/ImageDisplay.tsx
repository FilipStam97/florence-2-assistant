import {Typography} from "@heroui/react";

export function ImageDisplay({title,src}: {title: string, src: string}){
  return (
    <div className="flex max-w-xl flex-col gap-4">
      <Typography.Heading level={1}>{title}</Typography.Heading>
      <div>
        <img 
            src={`http://127.0.0.1:8000${src}`}
        />
      </div>
    </div>
  );
};