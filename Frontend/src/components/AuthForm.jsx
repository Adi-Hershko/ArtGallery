import React, { useState } from 'react';
import axios from 'axios';
import { toast, Bounce } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import AuthFormView from './AuthFormView'; // Using the unified view component
import { useUser } from '../contexts/UserContext';
import { useAuth } from '../hooks/useAuth';
import { set } from "../utils/authCookie";

function AuthForm({ mode }) {
  const { setUser } = useUser();
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formFields, setFormFields] = useState({ username: '', password: '' });
  const [formErrors, setFormErrors] = useState({ username: '', password: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormFields(prev => ({ ...prev, [name]: value }));

    const errorMessages = {
      username: value.length >= 3 && value.length <= 50 ? '' : 'Username must be between 3 and 50 characters',
      password: value.length >= 6 && value.length <= 50 ? '' : 'Password must be between 6 and 50 characters',
    };
    setFormErrors(prev => ({ ...prev, [name]: errorMessages[name] }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!formErrors.username && !formErrors.password) {
      try {
        const base_url = import.meta.env.VITE_BASE_URL; // Ensure you have VITE_BASE_URL in your .env
        const endpoint = mode === 'signup' ? '/sign-up' : '/sign-in';
        const api_url = `${base_url}${endpoint}`;

        const res = await axios.post(api_url, formFields);
        const message = mode === 'signup' ? res.data.message : `Welcome, ${res.data.username}`;
        const token = res.data.access_key
        set(token)

        toast.success(message, {
          position: 'bottom-left',
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: 'light',
          transition: Bounce,
        });

        setTimeout(() => {
          setUser({ username: res.data.username })
          login({ username: res.data.username });
          navigate("/feed");
        }, 3000);
      } catch (error) {
        toast.error(error.response.data.message, {
          position: 'bottom-left',
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: 'light',
          transition: Bounce,
        });
      }
    }
  };

  return (
    <AuthFormView
      mode={mode}
      formFields={formFields}
      formErrors={formErrors}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
    />
  );
}

export default AuthForm;
