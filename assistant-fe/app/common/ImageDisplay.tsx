import {Typography} from "@heroui/react";

export function ImageDisplay({title,src}: {title: string, src: string}){
  return (
    <div className="flex max-w-2xl flex-col gap-4 border py-6 px-4">
      <Typography.Heading level={3}>{title}</Typography.Heading>
      <div>
        <img 
            src={`http://127.0.0.1:8000${src}`}
        />
      </div>
    </div>
  );
};