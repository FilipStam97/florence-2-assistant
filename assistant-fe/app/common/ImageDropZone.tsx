import { Button } from "@heroui/react";


export default function ImageDropZone({
  setImage,
  image,
}: {
  setImage: (file: File | null) => void;
  image: File | null;
}) {
  return (
    <div className="space-y-4">
      <label className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 transition hover:border-blue-500 hover:bg-blue-50">
        <input
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => setImage(e.target.files?.[0] ?? null)}
        />

        {image ? (
          <img
            src={URL.createObjectURL(image)}
            alt="Preview"
            className="h-full w-full rounded-xl object-contain p-2"
          />
        ) : (
          <>
            <svg
              className="mb-4 h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              strokeWidth={1.5}
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 16V4m0 0l-4 4m4-4l4 4M4 20h16"
              />
            </svg>

            <p className="text-lg font-medium text-gray-700">
              Upload an image
            </p>

            <p className="text-sm text-gray-500">
              Click to browse or drag & drop
            </p>
          </>
        )}
      </label>
    </div>
  );
}