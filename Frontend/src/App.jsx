import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AuthPage from './pages/AuthPage'; 
import FeedPage from './pages/FeedPage'; 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sign-in" element={<AuthPage mode="signin" />} />
        <Route path="/sign-up" element={<AuthPage mode="signup" />} />
        <Route path="/feed" element={<FeedPage />} />
        {/* Define other routes as needed */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
