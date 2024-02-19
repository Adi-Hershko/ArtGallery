import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import { ToastContainer, toast } from 'react-toastify';
import { Bounce } from 'react-toastify';


function SignUpFormView({ formFields, formErrors, handleChange, handleSubmit }) {
  return (
    <Box
      component="form"
      noValidate
      onSubmit={handleSubmit}
      sx={{ mt: 1 }}
    >
      <TextField
        margin="normal"
        required
        fullWidth
        id="username"
        label="Username"
        name="username"
        autoComplete="username"
        autoFocus
        value={formFields.username}
        onChange={handleChange}
        error={!!formErrors.username}
        helperText={formErrors.username}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
        value={formFields.password}
        onChange={handleChange}
        error={!!formErrors.password}
        helperText={formErrors.password}
      />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        Register
      </Button>
      <Grid container justifyContent="center">
        <Grid item>
          <Link href="sign-in" variant="body2">
            {'Already have an account? Sign In'}
          </Link>
        </Grid>
      </Grid>
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
    </Box>
  );
}

export default SignUpFormView;
