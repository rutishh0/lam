import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Upload,
  File,
  X,
  CheckCircle,
  AlertCircle,
  FileText,
  Image as ImageIcon,
  Download
} from 'lucide-react';
import toast from 'react-hot-toast';

const DocumentUpload = ({ onDocumentsChange, existingDocuments = {} }) => {
  const [documents, setDocuments] = useState(existingDocuments);
  const [uploadProgress, setUploadProgress] = useState({});

  const documentTypes = {
    transcript: {
      label: 'Academic Transcript',
      accept: '.pdf,.doc,.docx',
      maxSize: 10 * 1024 * 1024, // 10MB
      required: true
    },
    personal_statement: {
      label: 'Personal Statement',
      accept: '.pdf,.doc,.docx,.txt',
      maxSize: 5 * 1024 * 1024, // 5MB
      required: true
    },
    reference_letter: {
      label: 'Reference Letter',
      accept: '.pdf,.doc,.docx',
      maxSize: 5 * 1024 * 1024, // 5MB
      required: true
    },
    cv: {
      label: 'CV/Resume',
      accept: '.pdf,.doc,.docx',
      maxSize: 5 * 1024 * 1024, // 5MB
      required: false
    },
    english_certificate: {
      label: 'English Language Certificate',
      accept: '.pdf,.jpg,.jpeg,.png',
      maxSize: 5 * 1024 * 1024, // 5MB
      required: false
    },
    passport: {
      label: 'Passport Copy',
      accept: '.pdf,.jpg,.jpeg,.png',
      maxSize: 5 * 1024 * 1024, // 5MB
      required: false
    }
  };

  const validateFile = (file, docType) => {
    const config = documentTypes[docType];
    
    // Check file size
    if (file.size > config.maxSize) {
      throw new Error(`File size must be less than ${config.maxSize / (1024 * 1024)}MB`);
    }
    
    // Check file type
    const acceptedTypes = config.accept.split(',');
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    if (!acceptedTypes.includes(fileExtension)) {
      throw new Error(`File type must be one of: ${config.accept}`);
    }
    
    return true;
  };

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });
  };

  const handleFileDrop = useCallback(async (acceptedFiles, docType) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    
    try {
      // Validate file
      validateFile(file, docType);
      
      // Set upload progress
      setUploadProgress(prev => ({ ...prev, [docType]: 0 }));
      
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          const newProgress = Math.min((prev[docType] || 0) + 10, 90);
          if (newProgress >= 90) {
            clearInterval(progressInterval);
          }
          return { ...prev, [docType]: newProgress };
        });
      }, 100);
      
      // Convert to base64
      const base64 = await convertToBase64(file);
      
      // Complete upload
      setUploadProgress(prev => ({ ...prev, [docType]: 100 }));
      
      // Update documents
      const newDocuments = {
        ...documents,
        [docType]: {
          name: file.name,
          size: file.size,
          type: file.type,
          data: base64,
          uploadedAt: new Date().toISOString()
        }
      };
      
      setDocuments(newDocuments);
      onDocumentsChange(newDocuments);
      
      toast.success(`${documentTypes[docType].label} uploaded successfully`);
      
      // Clear progress after delay
      setTimeout(() => {
        setUploadProgress(prev => {
          const { [docType]: _, ...rest } = prev;
          return rest;
        });
      }, 1000);
      
    } catch (error) {
      toast.error(error.message);
      setUploadProgress(prev => {
        const { [docType]: _, ...rest } = prev;
        return rest;
      });
    }
  }, [documents, onDocumentsChange]);

  const removeDocument = (docType) => {
    const newDocuments = { ...documents };
    delete newDocuments[docType];
    setDocuments(newDocuments);
    onDocumentsChange(newDocuments);
    toast.success(`${documentTypes[docType].label} removed`);
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getFileIcon = (fileType) => {
    if (fileType.includes('image')) return ImageIcon;
    return FileText;
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {Object.entries(documentTypes).map(([docType, config]) => {
          const { getRootProps, getInputProps, isDragActive } = useDropzone({
            onDrop: (files) => handleFileDrop(files, docType),
            accept: config.accept.split(',').reduce((acc, type) => {
              acc[type] = [];
              return acc;
            }, {}),
            maxFiles: 1,
            disabled: !!uploadProgress[docType]
          });
          
          const hasDocument = !!documents[docType];
          const isUploading = !!uploadProgress[docType];
          
          return (
            <div key={docType} className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">
                  {config.label}
                  {config.required && <span className="text-red-500 ml-1">*</span>}
                </label>
                {hasDocument && !isUploading && (
                  <button
                    onClick={() => removeDocument(docType)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    Remove
                  </button>
                )}
              </div>
              
              {!hasDocument && !isUploading ? (
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                    isDragActive
                      ? 'border-blue-400 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <input {...getInputProps()} />
                  <Upload className="mx-auto h-8 w-8 text-gray-400 mb-2" />
                  <p className="text-sm text-gray-600">
                    {isDragActive
                      ? 'Drop the file here...'
                      : 'Drag & drop or click to upload'
                    }
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {config.accept} (Max {config.maxSize / (1024 * 1024)}MB)
                  </p>
                </div>
              ) : isUploading ? (
                <div className="border rounded-lg p-4 bg-gray-50">
                  <div className="flex items-center space-x-3">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-700">Uploading...</p>
                      <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${uploadProgress[docType]}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="border rounded-lg p-4 bg-gray-50">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      {React.createElement(getFileIcon(documents[docType].type), {
                        className: 'h-8 w-8 text-gray-400'
                      })}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {documents[docType].name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatFileSize(documents[docType].size)}
                      </p>
                    </div>
                    <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Upload Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="text-sm text-blue-800">
            <p className="font-medium mb-1">Document Requirements:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>All documents must be clear and legible</li>
              <li>Academic transcripts should be official copies</li>
              <li>Reference letters must be on official letterhead</li>
              <li>Ensure personal information is visible on all documents</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
