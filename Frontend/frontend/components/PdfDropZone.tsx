// components/PdfDropzone.tsx
import React, { useState } from 'react';
import { useDropzone, Accept } from 'react-dropzone';
import { Concept } from '@/app/types';

type Props = {
  concepts: Concept[],
  setConcepts: (concepts: Concept[]) => void
}

const PdfDropzone = ({
  concepts, setConcepts
}: Props) => {
  const [files, setFiles] = useState<File[]>([]);


  const onDrop = (acceptedFiles: File[]) => {
    setFiles((prevFiles) => [
      ...prevFiles,
      ...acceptedFiles.map((file) =>
        Object.assign(file, {
          preview: URL.createObjectURL(file), // Create a preview URL for the file
        })
      ),
    ]);
  };

  const generateConcepts = async () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('file', file);
    });

    try {
      const response = await fetch('http://127.0.0.1:5000/api/concepts/generate', {
        method: "POST",
        body: formData
      });
      const data = await response.json();
      setConcepts(data);
      setFiles([]); // Clear the files after successful upload
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file.');
    }
  };

  // Define the accepted file types
  const accept: Accept = {
    'application/pdf': [],
    'application/octet-stream': [],
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept, // Accept only PDF files
  });

  return (
    <div>
      <div
        {...getRootProps({ className: 'dropzone w-full p-6 border-2 border-dashed border-blue-600 rounded-lg text-center bg-gray-100 cursor-pointer' })}
      >
        <input {...getInputProps()} />
        <p className="text-gray-500">Drag and drop your PDF here, or click to select one.</p>
      </div>
      <div className="mt-4">
        {files.length > 0 && (
          <div>
            <h4 className="text-lg font-semibold">Files to upload:</h4>
            <ul className="list-disc ml-5">
              {files.map((file, index) => (
                <li key={index} className="text-gray-800">{file.name}</li>
              ))}
            </ul>
            <button
              onClick={() => generateConcepts()}
              disabled={files.length < 1}
              className="mt-6 bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Generate Concepts
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PdfDropzone;
