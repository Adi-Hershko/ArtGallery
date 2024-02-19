import React from 'react';
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

  return (
    <Grid container component="main" sx={{ height: '100vh' }}>
      {/* Render the Background based on the mode */}
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
          {/* Pass the mode prop to AuthForm to switch between sign-up and sign-in */}
          <AuthForm mode={mode} />
        </Box>
      </Grid>
      {/* For the sign-up page, the Background is rendered after the form */}
      {mode === 'signup' && <Background />}
    </Grid>
  );
}

export default AuthPage;
