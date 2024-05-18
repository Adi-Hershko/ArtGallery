import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AuthPage from './pages/AuthPage';
import FeedPage from './pages/FeedPage';
import CustomToast from './components/CustomToast';
import { UserProvider } from './contexts/UserContext';
import { SearchProvider } from './contexts/SearchContext';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <SearchProvider>
      <UserProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/sign-in" element={<AuthPage mode="signin" />} />
            <Route path="/sign-up" element={<AuthPage mode="signup" />} />
            <Route
              path="/feed"
              element={
                <ProtectedRoute>
                  <FeedPage />
                </ProtectedRoute>
              }
            />
            {/* Define other routes as needed */}
          </Routes>
        </BrowserRouter>
        <CustomToast />
      </UserProvider>
    </SearchProvider>
  );
}

export default App;