import React, { useState } from 'react';
import axios from 'axios';

export default function FileUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const uploadResponse = await axios.post('http://localhost:5000/api/upload', formData);

      if (uploadResponse.data.success) {
        setUploading(false);
        setProcessing(true);

        // Process file
        const processResponse = await axios.post('http://localhost:5000/api/process', {
          file_path: uploadResponse.data.file_path
        });

        setProcessing(false);
        onUploadComplete(processResponse.data);
      }
    } catch (error) {
      console.error('Error:', error);
      setUploading(false);
      setProcessing(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Upload Customer Feedback File</h2>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <input
          type="file"
          accept=".xlsx,.csv"
          onChange={handleFileChange}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="cursor-pointer text-blue-600 hover:text-blue-800"
        >
          {file ? file.name : 'Click to select file or drag and drop'}
        </label>
        <p className="text-sm text-gray-500 mt-2">PMM Excel or CSV file</p>
      </div>

      {file && (
        <button
          onClick={handleUpload}
          disabled={uploading || processing}
          className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {uploading && 'Uploading...'}
          {processing && 'Processing with LLM...'}
          {!uploading && !processing && 'Process File'}
        </button>
      )}

      {processing && (
        <div className="mt-4 p-4 bg-blue-50 rounded">
          <p className="text-sm text-blue-800">
            ⏳ Categorizing items with OpenAI... This may take 2-3 minutes.
          </p>
        </div>
      )}
    </div>
  );
}
