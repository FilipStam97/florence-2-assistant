import {Typography} from "@heroui/react";

export function CaptionDisplay({title,text}: {title: string, text: string}){
  return (
    <div className="flex max-w-xl flex-col gap-4">
      <Typography.Heading level={1}>{title}</Typography.Heading>
      <Typography.Paragraph>
        {text}
      </Typography.Paragraph>
    </div>
  );
};