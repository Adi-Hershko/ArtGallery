import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {createBrowserRouter,RouterProvider} from 'react-router-dom'
import SignInPage from './pages/SignInPage'
import SignUpPage from './pages/SignUpPage'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
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

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
