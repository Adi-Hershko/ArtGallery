import React, { useState} from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {createBrowserRouter,RouterProvider} from 'react-router-dom'
import SignInPage from './pages/SignInPage'
import SignUpPage from './pages/SignUpPage'
import HomePage from './pages/HomePage.jsx'

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path:"/sign-in",
    element:<SignInPage/>
  },
  {
    path:"/sign-up",
    element:<SignUpPage/>
  },
]);



function App() {  

  return (
    <RouterProvider router={router}/>
  )
}

export default App;