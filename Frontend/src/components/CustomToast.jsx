import React from 'react';
import { ToastContainer, Bounce } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


function CustomToast({ style }) {
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
            style={{ zIndex: 9999, ...style }}
        />
    );
}


export default CustomToast;