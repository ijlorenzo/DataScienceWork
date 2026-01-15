import React, { useState } from 'react';
import FileUpload from './components/FileUpload';

export default function App() {
  const [result, setResult] = useState(null);

  const handleUploadComplete = (data) => {
    setResult(data);
  };

  const downloadExport = () => {
    const filename = result.export_path.split('/').pop();
    window.open(`http://localhost:5000/api/export/${filename}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Customer Feedback Synthesis Tool
          </h1>
          <p className="text-gray-600 mt-1">
            LLM-powered categorization with intelligent learning
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 px-4">
        {!result ? (
          <FileUpload onUploadComplete={handleUploadComplete} />
        ) : (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-green-600 mb-2">
                ✅ Processing Complete!
              </h2>
              <p className="text-gray-600">
                {result.processed_count} items categorized successfully
              </p>
            </div>

            <div className="bg-blue-50 rounded p-4 mb-6">
              <h3 className="font-semibold mb-2">What happened:</h3>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>✓ File parsed and validated</li>
                <li>✓ OpenAI categorized all items</li>
                <li>✓ LLM reasoning captured for each field</li>
                <li>✓ Excel file generated with formatting</li>
              </ul>
            </div>

            <button
              onClick={downloadExport}
              className="w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 font-semibold"
            >
              📥 Download Categorized Excel File
            </button>

            <button
              onClick={() => setResult(null)}
              className="w-full mt-3 bg-gray-200 text-gray-700 py-2 px-6 rounded-lg hover:bg-gray-300"
            >
              Process Another File
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
