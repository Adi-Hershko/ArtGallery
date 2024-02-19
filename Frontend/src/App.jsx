import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage'; // Assuming you have a HomePage component
import AuthPage from './pages/AuthPage'; // The unified AuthPage component

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sign-in" element={<AuthPage mode="signin" />} />
        <Route path="/sign-up" element={<AuthPage mode="signup" />} />
        {/* Define other routes as needed */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
