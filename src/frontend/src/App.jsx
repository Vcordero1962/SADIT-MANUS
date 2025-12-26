import React from 'react';
import { Route, Switch } from 'wouter';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

function App() {
    return (
        <Switch>
            <Route path="/" component={LandingPage} />
            <Route path="/login" component={Login} />
            <Route path="/dashboard" component={Dashboard} />

            {/* 404 Fallback */}
            <Route>
                <div className="min-h-screen flex items-center justify-center bg-gray-50">
                    <h1 className="text-2xl text-gray-400">404 - Page Not Found</h1>
                </div>
            </Route>
        </Switch>
    );
}

export default App;
