import React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import SignInForm from './SignInForm';
import Background from './Background';
import 'react-toastify/dist/ReactToastify.css';

function SignInPage() {
  return (
    <Grid container component="main" sx={{ height: '100vh' }}>
      <Background />
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
            Sign In
          </Typography>
          <SignInForm />
        </Box>
      </Grid>
    </Grid>
  );
}

export default SignInPage;
