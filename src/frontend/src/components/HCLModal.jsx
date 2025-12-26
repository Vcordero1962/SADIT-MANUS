import React, { useState } from 'react';
import { X, Plus, Trash2, FileText, AlertCircle } from 'lucide-react';

export default function HCLModal({ isOpen, onClose, onSave, initialData = {} }) {
    const [hclData, setHclData] = useState({
        antecedentes: initialData.antecedentes || [],
        medicamentos: initialData.medicamentos || [],
        alergias: initialData.alergias || [],
        cirugias: initialData.cirugias || [],
        labResults: initialData.labResults || {
            leucocitos: '',
            pcr: '',
            vsg: '',
            hemoglobina: '',
            plaquetas: ''
        },
        notas: initialData.notas || ''
    });

    const [newItem, setNewItem] = useState({
        antecedente: '',
        medicamento: '',
        alergia: '',
        cirugia: ''
    });

    if (!isOpen) return null;

    const addItem = (field, itemKey) => {
        if (newItem[itemKey].trim()) {
            setHclData({
                ...hclData,
                [field]: [...hclData[field], newItem[itemKey].trim()]
            });
            setNewItem({ ...newItem, [itemKey]: '' });
        }
    };

    const removeItem = (field, index) => {
        setHclData({
            ...hclData,
            [field]: hclData[field].filter((_, i) => i !== index)
        });
    };

    const updateLabResult = (field, value) => {
        setHclData({
            ...hclData,
            labResults: {
                ...hclData.labResults,
                [field]: value
            }
        });
    };

    const handleSave = () => {
        onSave(hclData);
        onClose();
    };

    const renderListSection = (title, field, itemKey, placeholder) => (
        <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-700">{title}</label>
            <div className="flex gap-2">
                <input
                    type="text"
                    value={newItem[itemKey]}
                    onChange={(e) => setNewItem({ ...newItem, [itemKey]: e.target.value })}
                    onKeyPress={(e) => e.key === 'Enter' && addItem(field, itemKey)}
                    placeholder={placeholder}
                    className="flex-1 border border-slate-300 rounded-md px-3 py-2 text-sm focus:ring-medical-500 focus:border-medical-500"
                />
                <button
                    type="button"
                    onClick={() => addItem(field, itemKey)}
                    className="px-3 py-2 bg-medical-600 text-white rounded-md hover:bg-medical-700 transition-colors"
                >
                    <Plus className="h-4 w-4" />
                </button>
            </div>
            {hclData[field].length > 0 && (
                <ul className="space-y-1">
                    {hclData[field].map((item, index) => (
                        <li key={index} className="flex items-center justify-between bg-slate-50 px-3 py-2 rounded-md">
                            <span className="text-sm text-slate-700">{item}</span>
                            <button
                                type="button"
                                onClick={() => removeItem(field, index)}
                                className="text-red-500 hover:text-red-700"
                            >
                                <Trash2 className="h-4 w-4" />
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
                {/* Header */}
                <div className="bg-medical-600 text-white px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <FileText className="h-6 w-6" />
                        <h2 className="text-xl font-bold">Historia Clínica Completa</h2>
                    </div>
                    <button onClick={onClose} className="hover:bg-medical-700 p-1 rounded transition-colors">
                        <X className="h-6 w-6" />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {/* Antecedentes Personales */}
                    <section>
                        <h3 className="text-lg font-semibold text-slate-800 mb-3">Antecedentes Personales</h3>
                        {renderListSection('Condiciones Médicas', 'antecedentes', 'antecedente', 'Ej: Diabetes, HTA, Obesidad...')}
                    </section>

                    {/* Medicamentos */}
                    <section>
                        <h3 className="text-lg font-semibold text-slate-800 mb-3">Medicación Actual</h3>
                        {renderListSection('Medicamentos', 'medicamentos', 'medicamento', 'Ej: Metformina 850mg...')}
                    </section>

                    {/* Alergias */}
                    <section>
                        <h3 className="text-lg font-semibold text-slate-800 mb-3">Alergias</h3>
                        {renderListSection('Alergias Conocidas', 'alergias', 'alergia', 'Ej: Penicilina, AINEs...')}
                    </section>

                    {/* Cirugías Previas */}
                    <section>
                        <h3 className="text-lg font-semibold text-slate-800 mb-3">Cirugías Previas</h3>
                        {renderListSection('Procedimientos Quirúrgicos', 'cirugias', 'cirugia', 'Ej: Artroplastia cadera 2015...')}
                    </section>

                    {/* Análisis de Laboratorio */}
                    <section className="bg-slate-50 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center">
                            Análisis de Laboratorio
                            <AlertCircle className="h-4 w-4 ml-2 text-yellow-500" />
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">
                                    Leucocitos (células/μL)
                                </label>
                                <input
                                    type="number"
                                    value={hclData.labResults.leucocitos}
                                    onChange={(e) => updateLabResult('leucocitos', e.target.value)}
                                    placeholder="Normal: 4000-11000"
                                    className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">
                                    PCR (mg/L)
                                </label>
                                <input
                                    type="number"
                                    step="0.1"
                                    value={hclData.labResults.pcr}
                                    onChange={(e) => updateLabResult('pcr', e.target.value)}
                                    placeholder="Normal: <10"
                                    className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">
                                    VSG (mm/h)
                                </label>
                                <input
                                    type="number"
                                    value={hclData.labResults.vsg}
                                    onChange={(e) => updateLabResult('vsg', e.target.value)}
                                    placeholder="Normal: <20"
                                    className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">
                                    Hemoglobina (g/dL)
                                </label>
                                <input
                                    type="number"
                                    step="0.1"
                                    value={hclData.labResults.hemoglobina}
                                    onChange={(e) => updateLabResult('hemoglobina', e.target.value)}
                                    placeholder="Normal: 12-16"
                                    className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">
                                    Plaquetas (células/μL)
                                </label>
                                <input
                                    type="number"
                                    value={hclData.labResults.plaquetas}
                                    onChange={(e) => updateLabResult('plaquetas', e.target.value)}
                                    placeholder="Normal: 150000-450000"
                                    className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm"
                                />
                            </div>
                        </div>
                    </section>

                    {/* Notas Adicionales */}
                    <section>
                        <h3 className="text-lg font-semibold text-slate-800 mb-3">Notas Adicionales</h3>
                        <textarea
                            value={hclData.notas}
                            onChange={(e) => setHclData({ ...hclData, notas: e.target.value })}
                            placeholder="Información adicional relevante para el diagnóstico..."
                            rows={4}
                            className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm focus:ring-medical-500 focus:border-medical-500"
                        />
                    </section>
                </div>

                {/* Footer */}
                <div className="bg-slate-50 px-6 py-4 flex justify-end space-x-3 border-t">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 border border-slate-300 text-slate-700 rounded-md hover:bg-slate-100 transition-colors"
                    >
                        Cancelar
                    </button>
                    <button
                        onClick={handleSave}
                        className="px-4 py-2 bg-medical-600 text-white rounded-md hover:bg-medical-700 transition-colors font-medium"
                    >
                        Guardar y Continuar
                    </button>
                </div>
            </div>
        </div>
    );
}
