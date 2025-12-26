import React, { useState, useEffect } from 'react';
import { useLocation } from 'wouter';
import axios from 'axios';
import { Activity, Users, FileText, Settings, LogOut, AlertTriangle, CheckCircle, BarChart2, ClipboardList } from 'lucide-react';
import ImageUploader from '../components/ImageUploader';
import HCLModal from '../components/HCLModal';

export default function Dashboard() {
    const [, setLocation] = useLocation();
    const [activeTab, setActiveTab] = useState('new-case');
    const [formData, setFormData] = useState({
        onset: 'gradual',
        location: 'distal',
        intensity: 5,
        character: 'mechanical',
        is_night_pain: false
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    // Multimodal data
    const [images, setImages] = useState([]);
    const [hclData, setHCLData] = useState(null);
    const [showHCLModal, setShowHCLModal] = useState(false);
    const [useMultimodal, setUseMultimodal] = useState(false);

    // Protected Route Check
    useEffect(() => {
        const token = localStorage.getItem('sadit_token');
        if (!token) setLocation('/login');
    }, [setLocation]);

    const handleLogout = () => {
        localStorage.removeItem('sadit_token');
        setLocation('/login');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const token = localStorage.getItem('sadit_token');

            // Decide endpoint based on multimodal mode
            if (useMultimodal && (images.length > 0 || hclData)) {
                console.log('🔵 [MULTIMODAL] Iniciando análisis multimodal...');
                console.log('🔵 [MULTIMODAL] Imágenes cargadas:', images.length);
                console.log('🔵 [MULTIMODAL] HCL Data:', hclData);

                // Multimodal submission
                const formDataMulti = new FormData();

                const clinicalData = {
                    pain_profile: {
                        onset: formData.onset,
                        location: formData.location,
                        intensity: formData.intensity,
                        character: formData.character,
                        is_night_pain: formData.is_night_pain
                    },
                    ild_months: 12,
                    mobility: "Independent"
                };

                console.log('🔵 [MULTIMODAL] Clinical data:', clinicalData);
                formDataMulti.append('clinical_data', JSON.stringify(clinicalData));

                if (hclData) {
                    const labData = hclData.labResults;
                    console.log('🔵 [MULTIMODAL] Lab data:', labData);
                    formDataMulti.append('lab_data', JSON.stringify(labData));
                    formDataMulti.append('medical_history', JSON.stringify({
                        antecedentes: hclData.antecedentes,
                        medicamentos: hclData.medicamentos,
                        alergias: hclData.alergias,
                        cirugias: hclData.cirugias
                    }));
                }

                images.forEach(img => {
                    console.log('🔵 [MULTIMODAL] Agregando imagen:', img.name);
                    formDataMulti.append('files', img);
                });

                console.log('🔵 [MULTIMODAL] Enviando request a /api/inference/multimodal');
                const response = await axios.post('/api/inference/multimodal', formDataMulti, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                });

                console.log('✅ [MULTIMODAL] Respuesta recibida:', response.data);
                setResult(response.data);
            } else {
                console.log('🟢 [SIMPLE] Iniciando análisis semiológico simple...');
                // Simple semiological analysis
                const payload = {
                    pain_profile: {
                        onset: formData.onset,
                        location: formData.location,
                        intensity: formData.intensity,
                        character: formData.character,
                        is_night_pain: formData.is_night_pain
                    },
                    ild_months: 12,
                    mobility: "Independent"
                };

                console.log('🟢 [SIMPLE] Payload:', payload);
                const response = await axios.post('/api/inference/clinical', payload, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                console.log('✅ [SIMPLE] Respuesta recibida:', response.data);
                setResult(response.data);
            }

        } catch (err) {
            console.error('❌ [ERROR] Inference Error:', err);
            console.error('❌ [ERROR] Error response:', err.response);
            console.error('❌ [ERROR] Error data:', err.response?.data);
            console.error('❌ [ERROR] Error status:', err.response?.status);

            if (err.response && err.response.status === 401) {
                alert("Sesión expirada. Por favor ingrese nuevamente.");
                setLocation('/login');
            } else {
                const errorMsg = err.response?.data?.detail || err.message;
                alert(`Error al conectar con el motor de inferencia:\n${errorMsg}`);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-slate-100">

            {/* Sidebar */}
            <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col">
                <div className="h-16 flex items-center px-6 border-b border-slate-800">
                    <Activity className="h-6 w-6 text-medical-500 mr-2" />
                    <span className="font-bold text-white text-lg">SADIT Clínico</span>
                </div>

                <nav className="flex-1 px-4 py-6 space-y-2">
                    <NavItem icon={<FileText />} label="Nuevo Caso" active={activeTab === 'new-case'} onClick={() => setActiveTab('new-case')} />
                    <NavItem icon={<Users />} label="Pacientes" active={activeTab === 'patients'} onClick={() => setActiveTab('patients')} />
                    <NavItem icon={<BarChart2 />} label="Estadísticas" active={activeTab === 'stats'} onClick={() => setActiveTab('stats')} />
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <button onClick={handleLogout} className="flex items-center space-x-2 text-sm hover:text-white transition-colors">
                        <LogOut className="h-4 w-4" />
                        <span>Cerrar Sesión</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto">
                <header className="bg-white shadow-sm h-16 flex items-center justify-between px-8">
                    <h1 className="text-xl font-semibold text-slate-800">
                        {activeTab === 'new-case' ? 'Evaluación Diagnóstica (Protocolo ALICIA)' : 'Panel General'}
                    </h1>
                    <div className="flex items-center space-x-3">
                        <div className="h-8 w-8 bg-medical-100 rounded-full flex items-center justify-center text-medical-700 font-bold">
                            DR
                        </div>
                        <span className="text-sm font-medium text-slate-600">Dr. Usuario</span>
                    </div>
                </header>

                <div className="p-8 max-w-5xl mx-auto">
                    {activeTab === 'new-case' && (
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                            {/* Clinical Form */}
                            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                                <h2 className="text-lg font-medium text-slate-900 mb-4 flex items-center">
                                    <Settings className="h-5 w-5 mr-2 text-slate-400" />
                                    Parámetros Semiológicos
                                </h2>
                                <form onSubmit={handleSubmit} className="space-y-5">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-1">Carácter del Dolor</label>
                                        <select
                                            className="w-full border-slate-300 rounded-md shadow-sm focus:ring-medical-500 focus:border-medical-500"
                                            value={formData.character}
                                            onChange={e => setFormData({ ...formData, character: e.target.value })}
                                        >
                                            <option value="mechanical">Mecánico (Carga/Movimiento)</option>
                                            <option value="inflammatory">Inflamatorio (Constante)</option>
                                            <option value="terebrante">Terebrante (Perforante/Agudo)</option>
                                        </select>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-1">Aparición</label>
                                            <select
                                                className="w-full border-slate-300 rounded-md shadow-sm focus:ring-medical-500 focus:border-medical-500"
                                                value={formData.onset}
                                                onChange={e => setFormData({ ...formData, onset: e.target.value })}
                                            >
                                                <option value="gradual">Gradual</option>
                                                <option value="sudden">Súbita</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-1">Localización</label>
                                            <select
                                                className="w-full border-slate-300 rounded-md shadow-sm focus:ring-medical-500 focus:border-medical-500"
                                                value={formData.location}
                                                onChange={e => setFormData({ ...formData, location: e.target.value })}
                                            >
                                                <option value="distal">Distal (Muslo)</option>
                                                <option value="inguinal">Inguinal</option>
                                                <option value="diffuse">Difuso</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 mb-1">Intensidad (EVA 1-10): {formData.intensity}</label>
                                        <input
                                            type="range" min="1" max="10"
                                            className="w-full accent-medical-600"
                                            value={formData.intensity}
                                            onChange={e => setFormData({ ...formData, intensity: parseInt(e.target.value) })}
                                        />
                                    </div>

                                    <div className="flex items-center">
                                        <input
                                            id="night-pain" type="checkbox"
                                            className="h-4 w-4 text-medical-600 focus:ring-medical-500 border-gray-300 rounded"
                                            checked={formData.is_night_pain}
                                            onChange={e => setFormData({ ...formData, is_night_pain: e.target.checked })}
                                        />
                                        <label htmlFor="night-pain" className="ml-2 block text-sm text-slate-900 font-medium">
                                            Presencia de Dolor Nocturno
                                        </label>
                                    </div>

                                    {/* Multimodal Section */}
                                    <div className="pt-4 border-t border-slate-200">
                                        <div className="flex items-center justify-between mb-3">
                                            <label className="flex items-center cursor-pointer">
                                                <input
                                                    type="checkbox"
                                                    checked={useMultimodal}
                                                    onChange={(e) => setUseMultimodal(e.target.checked)}
                                                    className="h-4 w-4 text-medical-600 focus:ring-medical-500 border-gray-300 rounded"
                                                />
                                                <span className="ml-2 text-sm font-medium text-slate-700">
                                                    Habilitar Análisis Multimodal Completo
                                                </span>
                                            </label>
                                        </div>

                                        {useMultimodal && (
                                            <div className="space-y-4 p-4 bg-medical-50 rounded-lg">
                                                <button
                                                    type="button"
                                                    onClick={() => setShowHCLModal(true)}
                                                    className="w-full flex items-center justify-center space-x-2 bg-white border-2 border-medical-600 text-medical-600 py-2 px-4 rounded-lg hover:bg-medical-50 transition-colors font-medium"
                                                >
                                                    <ClipboardList className="h-5 w-5" />
                                                    <span>
                                                        {hclData
                                                            ? 'Editar Historia Clínica Completa'
                                                            : 'Agregar Historia Clínica Completa'}
                                                    </span>
                                                </button>

                                                {hclData && (
                                                    <div className="text-xs text-medical-700 bg-medical-100 p-2 rounded">
                                                        ✓ HCL registrada: {hclData.antecedentes.length} antecedentes, {hclData.medicamentos.length} medicamentos
                                                    </div>
                                                )}

                                                <div>
                                                    <h3 className="text-sm font-medium text-slate-700 mb-2">Imágenes Radiológicas</h3>
                                                    <ImageUploader onImagesChange={setImages} />
                                                </div>
                                            </div>
                                        )}
                                    </div>

                                    <div className="pt-4">
                                        <button type="submit" disabled={loading} className="w-full bg-slate-900 text-white py-2 px-4 rounded-lg hover:bg-slate-800 transition-colors disabled:opacity-50 font-medium">
                                            {loading ? 'Procesando Inferencia...' : useMultimodal ? 'Ejecutar Análisis Multimodal Completo' : 'Ejecutar Análisis Semiológico'}
                                        </button>
                                    </div>
                                </form>
                            </div>

                            {/* HCL Modal */}
                            <HCLModal
                                isOpen={showHCLModal}
                                onClose={() => setShowHCLModal(false)}
                                onSave={(data) => {
                                    setHCLData(data);
                                    localStorage.setItem('sadit_hcl_data', JSON.stringify(data));
                                }}
                                initialData={hclData || {}}
                            />

                            {/* Results Panel */}
                            <div className="space-y-6">
                                {/* Status Card */}
                                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 h-full flex flex-col justify-center items-center text-center">
                                    {!result && !loading && (
                                        <div className="text-slate-400">
                                            <Activity className="h-12 w-12 mx-auto mb-3 opacity-20" />
                                            <p>Ingrese los datos y ejecute el análisis para ver resultados.</p>
                                        </div>
                                    )}

                                    {loading && (
                                        <div className="text-medical-600 animate-pulse">
                                            <Activity className="h-12 w-12 mx-auto mb-3" />
                                            <p className="font-medium">Calculando probabilidades bayesianas...</p>
                                        </div>
                                    )}

                                    {result && !loading && (
                                        <div className="w-full animate-fadeIn">
                                            <div className={`inline-flex items-center justify-center p-3 rounded-full mb-4 ${result.safetyScore > 0.4 ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                                                {result.safetyScore > 0.4 ? <AlertTriangle className="h-8 w-8" /> : <CheckCircle className="h-8 w-8" />}
                                            </div>

                                            <h3 className="text-2xl font-bold text-slate-800 mb-1">{result.diagnosis}</h3>
                                            <p className="text-slate-500 mb-6 font-mono text-sm">Confianza del Modelo: {(result.probability * 100).toFixed(1)}%</p>

                                            <div className="bg-slate-50 rounded-lg p-4 border border-slate-100 text-left">
                                                <div className="flex justify-between items-center mb-2">
                                                    <span className="text-sm font-medium text-slate-600">Safety Score (Riesgo):</span>
                                                    <span className={`font-bold ${result.safetyScore > 0.4 ? 'text-red-600' : 'text-green-600'}`}>
                                                        {result.safetyScore.toFixed(2)}
                                                    </span>
                                                </div>
                                                <div className="w-full bg-gray-200 rounded-full h-2.5">
                                                    <div
                                                        className={`h-2.5 rounded-full ${result.safetyScore > 0.4 ? 'bg-red-500' : 'bg-green-500'}`}
                                                        style={{ width: `${result.safetyScore * 100}%` }}
                                                    ></div>
                                                </div>
                                                <p className="mt-4 text-sm text-slate-700">
                                                    <strong>Recomendación:</strong> {result.recommendation}
                                                </p>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab !== 'new-case' && (
                        <div className="text-center py-20 text-slate-400">
                            <Settings className="h-10 w-10 mx-auto mb-4 opacity-50" />
                            <p>Módulo en construcción para v1.3</p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

function NavItem({ icon, label, active, onClick }) {
    return (
        <button
            onClick={onClick}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${active ? 'bg-medical-600 text-white shadow-md' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
        >
            {React.cloneElement(icon, { size: 20 })}
            <span className="font-medium text-sm">{label}</span>
        </button>
    );
}
