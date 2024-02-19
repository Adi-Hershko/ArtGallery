import React from 'react';
import { ToastContainer, Bounce } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


function CustomToast() {
    return (
    <ToastContainer
        position="bottom-left"
        autoClose={2000}
        hideProgressBar={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        transition={Bounce}
        />
    );
}

export default CustomToast;