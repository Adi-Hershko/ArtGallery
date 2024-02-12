import React, { useState} from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


function App() {

  const navigate = useNavigate();


  return (
    <div>
      <h1>Art Gallery</h1>
      <h2>Press either one to check</h2>
      <button onClick={() => navigate('/sign-in')}>Sign in</button>
      <button onClick={() => navigate('/sign-up')}>Sign up</button>
    </div>
  )
}

export default App;