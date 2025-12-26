import React, { useState } from 'react';
import { useLocation } from 'wouter';
import axios from 'axios';
import { Lock, User, AlertCircle, ArrowRight } from 'lucide-react';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [, setLocation] = useLocation();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Form Data required by OAuth2PasswordRequestForm
            const formData = new FormData();
            formData.append('username', email); // FastAPIs OAuth2 uses 'username' field
            formData.append('password', password);

            const response = await axios.post('/api/auth/login', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const { access_token } = response.data;

            // Store Token (In production, consider HttpOnly Cookies)
            localStorage.setItem('sadit_token', access_token);

            // Redirect to Dashboard
            setLocation('/dashboard');

        } catch (err) {
            console.error(err);
            if (err.response && err.response.status === 401) {
                setError('Credenciales incorrectas. Verifique su email y contraseña.');
            } else {
                setError('Error de conexión con el servidor SADIT.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center">
                    <div className="p-3 bg-medical-100 rounded-full">
                        <Lock className="h-8 w-8 text-medical-600" />
                    </div>
                </div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-slate-900">
                    Acceso Profesional
                </h2>
                <p className="mt-2 text-center text-sm text-slate-600">
                    Orquestación SADIT v1.2
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10 border border-slate-100">
                    <form className="space-y-6" onSubmit={handleLogin}>

                        {/* Email Field */}
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-slate-700">
                                Email Institucional
                            </label>
                            <div className="mt-1 relative rounded-md shadow-sm">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <User className="h-5 w-5 text-slate-400" />
                                </div>
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="focus:ring-medical-500 focus:border-medical-500 block w-full pl-10 sm:text-sm border-slate-300 rounded-md py-2 border"
                                    placeholder="medico@hospital.com"
                                />
                            </div>
                        </div>

                        {/* Password Field */}
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-slate-700">
                                Contraseña
                            </label>
                            <div className="mt-1 relative rounded-md shadow-sm">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock className="h-5 w-5 text-slate-400" />
                                </div>
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="current-password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="focus:ring-medical-500 focus:border-medical-500 block w-full pl-10 sm:text-sm border-slate-300 rounded-md py-2 border"
                                />
                            </div>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="rounded-md bg-red-50 p-4">
                                <div className="flex">
                                    <div className="flex-shrink-0">
                                        <AlertCircle className="h-5 w-5 text-red-400" />
                                    </div>
                                    <div className="ml-3">
                                        <h3 className="text-sm font-medium text-red-800">{error}</h3>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Submit Button */}
                        <div>
                            <button
                                type="submit"
                                disabled={loading}
                                className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${loading ? 'bg-medical-400' : 'bg-medical-600 hover:bg-medical-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-medical-500 transition-colors`}
                            >
                                {loading ? 'Verificando...' : 'Ingresar al Dashboard'}
                                {!loading && <ArrowRight className="ml-2 h-4 w-4" />}
                            </button>
                        </div>
                    </form>

                    <div className="mt-6">
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-slate-300" />
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white text-slate-500">
                                    Acceso restringido (Multi-Tenant)
                                </span>
                            </div>
                        </div>
                        <div className="mt-6 text-center text-xs text-slate-400">
                            Sistema protegido por auditoría ISO 27001. Su IP será registrada.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
