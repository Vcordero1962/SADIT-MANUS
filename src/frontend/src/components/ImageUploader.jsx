import React, { useState, useCallback } from 'react';
import { Upload, X, FileImage, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function ImageUploader({ onImagesChange }) {
    const [images, setImages] = useState([]);
    const [isDragging, setIsDragging] = useState(false);
    const [error, setError] = useState(null);

    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/dicom', 'application/dicom'];
    const MAX_SIZE = 10 * 1024 * 1024; // 10MB

    const validateFile = (file) => {
        if (!ALLOWED_TYPES.includes(file.type) && !file.name.toLowerCase().endsWith('.dcm')) {
            return `${file.name}: Formato no permitido. Use JPG, PNG o DICOM.`;
        }
        if (file.size > MAX_SIZE) {
            return `${file.name}: Tamaño máximo 10MB excedido.`;
        }
        return null;
    };

    const handleFiles = (fileList) => {
        const newFiles = Array.from(fileList);
        let validFiles = [];
        let errorMsg = null;

        for (const file of newFiles) {
            const validationError = validateFile(file);
            if (validationError) {
                errorMsg = validationError;
                break;
            }
            validFiles.push(file);
        }

        if (errorMsg) {
            setError(errorMsg);
            setTimeout(() => setError(null), 3000);
            return;
        }

        setError(null);
        const updatedImages = [...images, ...validFiles];
        setImages(updatedImages);
        onImagesChange(updatedImages);
    };

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFiles(e.dataTransfer.files);
    }, [images]);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleFileInput = (e) => {
        if (e.target.files) {
            handleFiles(e.target.files);
        }
    };

    const removeImage = (index) => {
        const updated = images.filter((_, i) => i !== index);
        setImages(updated);
        onImagesChange(updated);
    };

    return (
        <div className="space-y-4">
            {/* Drop Zone */}
            <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${isDragging
                        ? 'border-medical-500 bg-medical-50'
                        : 'border-slate-300 hover:border-medical-400'
                    }`}
            >
                <Upload className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                <p className="text-sm text-slate-600 mb-2">
                    Arrastra imágenes radiológicas aquí o{' '}
                    <label className="text-medical-600 hover:text-medical-700 cursor-pointer font-medium">
                        selecciónalas
                        <input
                            type="file"
                            multiple
                            accept=".jpg,.jpeg,.png,.dcm"
                            onChange={handleFileInput}
                            className="hidden"
                        />
                    </label>
                </p>
                <p className="text-xs text-slate-400">JPG, PNG, DICOM • Máx 10MB por archivo</p>
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start">
                    <AlertCircle className="h-5 w-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-red-700">{error}</p>
                </div>
            )}

            {/* Preview Grid */}
            {images.length > 0 && (
                <div className="space-y-2">
                    <h4 className="text-sm font-medium text-slate-700">
                        Imágenes cargadas ({images.length})
                    </h4>
                    <div className="grid grid-cols-2 gap-3">
                        {images.map((file, index) => (
                            <div
                                key={index}
                                className="relative bg-slate-50 border border-slate-200 rounded-lg p-3 flex items-center space-x-3"
                            >
                                <FileImage className="h-8 w-8 text-medical-600 flex-shrink-0" />
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-slate-800 truncate">
                                        {file.name}
                                    </p>
                                    <p className="text-xs text-slate-500">
                                        {(file.size / 1024).toFixed(1)} KB
                                    </p>
                                </div>
                                <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
                                <button
                                    onClick={() => removeImage(index)}
                                    className="absolute top-2 right-2 p-1 hover:bg-red-100 rounded transition-colors"
                                >
                                    <X className="h-4 w-4 text-red-500" />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
