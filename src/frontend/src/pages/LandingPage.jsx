import React from 'react';
import { ShieldCheck, Activity, Headphones, Lock, ArrowRight } from 'lucide-react';
import { Link } from 'wouter';

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-white">
            {/* Navbar */}
            <nav className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        <Activity className="h-8 w-8 text-medical-600" />
                        <span className="text-xl font-bold text-slate-900">SADIT <span className="text-medical-600">v1.2</span></span>
                    </div>
                    <div className="flex items-center space-x-4">
                        <a href="#podcast" className="text-sm font-medium text-slate-600 hover:text-medical-600 transition-colors">Inv. Científica</a>
                        <Link href="/login">
                            <button className="bg-medical-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-medical-700 transition-colors shadow-sm">
                                Acceso Profesional
                            </button>
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative overflow-hidden pt-16 pb-24">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <div className="inline-flex items-center space-x-2 bg-blue-50 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold mb-6">
                        <ShieldCheck className="h-4 w-4" />
                        <span>ISO 13485 Compliant & HIPAA Ready</span>
                    </div>
                    <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 tracking-tight mb-6">
                        Orquestación de <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-medical-600 to-blue-400">
                            Soluciones Médicas
                        </span>
                    </h1>
                    <p className="max-w-2xl mx-auto text-xl text-slate-600 mb-10 leading-relaxed">
                        Sistema de Apoyo al Diagnóstico Instrumentado para Traumatología.
                        Integramos Semioogía ALICIA, Inferencia Bayesiana y Visión Artificial
                        bajo estricta supervisión médica.
                    </p>

                    <div className="flex justify-center gap-4">
                        <Link href="/login">
                            <button className="flex items-center px-8 py-3 bg-slate-900 text-white rounded-xl font-semibold hover:bg-slate-800 transition-all hover:scale-105 active:scale-95">
                                Iniciar Diagnóstico
                                <ArrowRight className="ml-2 h-5 w-5" />
                            </button>
                        </Link>
                    </div>
                </div>
            </section>

            {/* Ethical / Human-in-the-Loop Section */}
            <section className="py-20 bg-slate-50 border-y border-slate-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div>
                            <h2 className="text-3xl font-bold text-slate-900 mb-4">Tecnología con Ética Médica</h2>
                            <p className="text-lg text-slate-600 mb-6">
                                SADIT no reemplaza al clínico; lo potencia. Nuestro arquitectura
                                <strong> "Human-in-the-Loop"</strong> garantiza que cada inferencia probabilística
                                sea validada por un profesional antes de convertirse en un diagnóstico final.
                            </p>
                            <ul className="space-y-4">
                                {[
                                    "Validación Bayesiana de Incertidumbre",
                                    "Protocolo de Seguridad Séptica (SafetyScore)",
                                    "Auditoría de Acceso por Roles (Multi-Tenant)"
                                ].map((item, i) => (
                                    <li key={i} className="flex items-center space-x-3 text-slate-700">
                                        <div className="h-2 w-2 bg-medical-500 rounded-full" />
                                        <span>{item}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 relative overflow-hidden">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-medical-50 rounded-bl-full -mr-8 -mt-8" />
                            <Lock className="h-12 w-12 text-medical-600 mb-4 relative z-10" />
                            <h3 className="text-xl font-bold text-slate-900 mb-2 relative z-10">Seguridad Aislada</h3>
                            <p className="text-slate-600 relative z-10">
                                Implementamos aislamiento por esquemas (Schema Isolation) para garantizar
                                que los datos de su institución permanezcan privados y herméticos.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Podcast / Divulgation Section */}
            <section id="podcast" className="py-20 relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <div className="mb-8 flex justify-center">
                        <div className="p-4 bg-purple-100 rounded-full">
                            <Headphones className="h-8 w-8 text-purple-600" />
                        </div>
                    </div>
                    <h2 className="text-3xl font-bold text-slate-900 mb-4">Divulgación para Mayores de 55+</h2>
                    <p className="max-w-xl mx-auto text-lg text-slate-600 mb-8">
                        Creemos en democratizar el conocimiento de salud ósea. Escuche nuestra serie
                        de podcasts diseñada para pacientes, explicando patologías complejas en lenguaje claro.
                    </p>
                    <a href="#" className="text-medical-600 font-semibold hover:underline decoration-2 underline-offset-4">
                        Explorar Episodios Disponibles &rarr;
                    </a>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800">
                <div className="max-w-7xl mx-auto px-4 text-center">
                    <p>&copy; 2025 SADIT Project. Designed for Medical Excellence.</p>
                    <p className="text-sm mt-2">v1.2-alpha | Dockerized Architecture</p>
                </div>
            </footer>
        </div>
    );
}
