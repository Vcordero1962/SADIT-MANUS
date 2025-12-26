/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                medical: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    500: '#0ea5e9', // Primary Blue
                    600: '#0284c7',
                    900: '#0c4a6e',
                },
                safety: {
                    warning: '#f59e0b',
                    critical: '#ef4444', // Red for Septic Alerts
                    safe: '#10b981'
                }
            }
        },
    },
    plugins: [],
}
