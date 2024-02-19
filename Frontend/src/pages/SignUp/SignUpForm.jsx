import React, { useState } from 'react';
import axios from 'axios';
import { Bounce, toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import SignUpFormView from './SignUpFormView';

function SignUpForm() {
  const navigate = useNavigate();
  const [formFields, setFormFields] = useState({ username: '', password: '' });
  const [formErrors, setFormErrors] = useState({ username: '', password: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormFields({ ...formFields, [name]: value });

    if (name === 'username') {
      setFormErrors({
        ...formErrors,
        username: value.length >= 3 && value.length <= 50 ? '' : 'Username must be between 3 and 50 characters',
      });
    } else if (name === 'password') {
      setFormErrors({
        ...formErrors,
        password: value.length >= 6 && value.length <= 50 ? '' : 'Password must be between 6 and 50 characters',
      });
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!formErrors.username && !formErrors.password) {
      try {
        const base_url = import.meta.env.VITE_BASE_URL;
        const api_url = `${base_url}/sign-up`;
        const res = await axios.post(api_url, formFields);
        toast.success(res.data.message, {
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
          navigate('/sign-in');
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
    <SignUpFormView
      formFields={formFields}
      formErrors={formErrors}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
    />
  );
}

export default SignUpForm;
