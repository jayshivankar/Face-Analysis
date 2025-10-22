import { useRef } from 'react';
import { motion } from 'framer-motion';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

export default function ImageUpload({ faceImage, setFaceImage, skinImage, setSkinImage }) {
  const faceInputRef = useRef(null);
  const skinInputRef = useRef(null);

  const handleFaceUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFaceImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSkinUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSkinImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e, type) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        if (type === 'face') {
          setFaceImage(reader.result);
        } else {
          setSkinImage(reader.result);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Face Image (Required)
        </label>
        <div
          onDrop={(e) => handleDrop(e, 'face')}
          onDragOver={handleDragOver}
          onClick={() => faceInputRef.current?.click()}
          className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-8 text-center cursor-pointer hover:border-blue-500 dark:hover:border-blue-400 transition-colors bg-gray-50 dark:bg-gray-900"
        >
          {faceImage ? (
            <div className="relative">
              <img
                src={faceImage}
                alt="Face preview"
                className="max-h-64 mx-auto rounded-lg shadow-lg"
              />
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setFaceImage(null);
                }}
                className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="flex justify-center">
                <div className="bg-blue-100 dark:bg-blue-900 p-4 rounded-full">
                  <Upload className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
              <div>
                <p className="text-gray-700 dark:text-gray-300 font-medium">
                  Click to upload or drag and drop
                </p>
                <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
                  PNG, JPG or JPEG (MAX. 10MB)
                </p>
              </div>
            </div>
          )}
        </div>
        <input
          ref={faceInputRef}
          type="file"
          accept="image/*"
          onChange={handleFaceUpload}
          className="hidden"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Skin Close-up (Optional)
        </label>
        <div
          onDrop={(e) => handleDrop(e, 'skin')}
          onDragOver={handleDragOver}
          onClick={() => skinInputRef.current?.click()}
          className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-6 text-center cursor-pointer hover:border-blue-500 dark:hover:border-blue-400 transition-colors bg-gray-50 dark:bg-gray-900"
        >
          {skinImage ? (
            <div className="relative">
              <img
                src={skinImage}
                alt="Skin preview"
                className="max-h-48 mx-auto rounded-lg shadow-lg"
              />
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setSkinImage(null);
                }}
                className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="flex justify-center">
                <ImageIcon className="w-6 h-6 text-gray-400" />
              </div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Upload skin image for detailed analysis
              </p>
            </div>
          )}
        </div>
        <input
          ref={skinInputRef}
          type="file"
          accept="image/*"
          onChange={handleSkinUpload}
          className="hidden"
        />
      </div>
    </div>
  );
}
