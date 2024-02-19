import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import CustomToast from './CustomToast';

function AuthFormView({ formFields, formErrors, handleChange, handleSubmit, mode }) {
  const isSignUp = mode === 'signup';
  const buttonText = isSignUp ? 'Register' : 'Sign In';
  const switchModeText = isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign up";
  const switchModeLink = isSignUp ? '/sign-in' : '/sign-up';

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
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{ mt: 3, mb: 2 }}
      >
        {buttonText}
      </Button>
      <Grid container justifyContent="center">
        <Grid item>
          <Link href={switchModeLink} variant="body2">
            {switchModeText}
          </Link>
        </Grid>
      </Grid>
      <CustomToast />
    </Box>
  );
}

export default AuthFormView;
