import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';

const ProtectedRoute = ({ children }) => {
    const { user } = useUser();

    if (!user) {
        // User is not signed in, redirect to sign-in page
        return <Navigate to="/sign-in" replace />;
    }

    return children;
};

export default ProtectedRoute;