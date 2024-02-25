import React, {useState, useEffect } from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import CssBaseline from '@mui/material/CssBaseline';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import AuthForm from '../components/AuthForm';
import Background from '../components/Background';
import 'react-toastify/dist/ReactToastify.css';

function AuthPage({ mode }) {
  const titleText = mode === 'signup' ? 'Sign Up' : 'Sign In';
  const [isBackgroundLoading, setBackgroundLoading] = useState(true);

  useEffect(() => {
    const img = new Image();
    img.src = 'https://source.unsplash.com/random?wallpapers';
    img.onload = () => setBackgroundLoading(false);
  }, []);

  return (
    <Grid container component="main" sx={{ height: '100vh' }}>
      {isBackgroundLoading ? (
        
        <Box sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          width: '100%', 
          height: '100vh',
        }}>
          <CircularProgress size={150}/>
        </Box>
      ) : (
        <>
          {mode === 'signin' && <Background />}
          <CssBaseline />
          <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
            <Box
              sx={{
                my: 8,
                mx: 4,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Typography component="h1" variant="h5">
                {titleText}
              </Typography>
              <AuthForm mode={mode} />
            </Box>
          </Grid>
          {mode === 'signup' && <Background />}
        </>
      )}
    </Grid>
  );
}

export default AuthPage;
