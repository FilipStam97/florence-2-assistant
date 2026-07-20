import { Button } from "@heroui/react";


export default function ImageDropZone({setImage, image}: {setImage: any, image: any}) {

    return(
        <div> 
        <input 
            type="file" 
            accept="image/*" 
            onChange={(e) => setImage(e.target.files?.[0] || null)}
            className="w-full border p-2  py-4"
            />
            {image &&
                <img  src={URL.createObjectURL(image)}/>

            }
        </div>
    )
}