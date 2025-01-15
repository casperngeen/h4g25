'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mail, Lock, User, ArrowRight } from 'lucide-react'; // Updated imports
import Image from 'next/image';
import { Container, Typography, Button, TextField, Select, MenuItem, InputLabel, FormControl, Box, IconButton, InputAdornment } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';

const API_BASE_URL = 'http://your-backend-url'; // Replace this with your backend API URL

const LoginSignupPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [userType, setUserType] = useState(''); // To handle the user type (resident or admin)
  const [error, setError] = useState('');

  const toggleMode = () => setIsLogin(!isLogin);

  const handleTogglePassword = () => {
    setPasswordVisible(!passwordVisible);
  };

  const handleLogin = async () => {
    const loginData = {
      username: name,
      password,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });
      
      const result = await response.json();
      if (response.ok) {
        // Handle successful login (e.g., save the access token, redirect)
        console.log(result);
      } else {
        // Show error message if login fails
        setError(result.Error || 'Login failed');
      }
    } catch (error) {
      console.error('Login failed', error);
      setError('An error occurred while logging in.');
    }
  };

  const handleRegister = async () => {
    const registerData = {
      username: name,
      password,
      mobile: '1234567890', // You can replace this with actual mobile input if needed
      isadmin: userType === 'admin' ? 1 : 0,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registerData),
      });

      const result = await response.json();
      if (response.ok) {
        // Handle successful registration (e.g., show a success message, reset form)
        console.log(result);
      } else {
        // Show error message if registration fails
        setError(result.Error || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration failed', error);
      setError('An error occurred while registering.');
    }
  };

  const formVariants = {
    hidden: { opacity: 0, x: -30 },
    visible: { opacity: 1, x: 0 },
  };

  return (
    <div className="flex flex-col md:flex-row h-screen bg-gray-100">
      {/* Right side panel */}
      <div className="w-full md:w-1/2 bg-gray-100 p-8 md:p-16 flex flex-col justify-center items-center">
        {/* Header with Logo and Welcome Message */}
        <Box display="flex" flexDirection="column" alignItems="center" textAlign="center">
          <Image
            src="/images/mwh_logo.png" // Ensure this image path is correct and the image is in the /public/images folder
            alt="Muhammadiyah Welfare Home Logo"
            width={150}
            height={150}
          />
          <Typography variant="h4" component="h1" sx={{ marginTop: 2 }}>
            Welcome to Muhammadiyah Welfare Home
          </Typography>
        </Box>

        {/* Error Message */}
        {error && <Typography color="error" variant="body2">{error}</Typography>}

        {/* Login or Create Account Box */}
        <Box sx={{ marginTop: 4 }} display="flex" flexDirection="column" alignItems="center">
          {/* Select User Type */}
          <FormControl fullWidth sx={{ maxWidth: 400, mb: 2 }}>
            <InputLabel>Select User Type</InputLabel>
            <Select
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
              label="Select User Type"
            >
              <MenuItem value="resident">Resident</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </Select>
          </FormControl>

          {/* Username Field */}
          <TextField
            fullWidth
            label="Enter Username"
            variant="outlined"
            margin="normal"
            sx={{ maxWidth: 400 }}
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          {/* Password Field with Hide/Show Feature */}
          <TextField
            fullWidth
            id="password-field"
            label="Enter Password"
            variant="outlined"
            margin="normal"
            type={passwordVisible ? "text" : "password"}
            sx={{ maxWidth: 400 }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={handleTogglePassword} edge="end">
                    {passwordVisible ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          {/* Login or Create Account Button */}
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ maxWidth: 400, mt: 2 }}
            onClick={isLogin ? handleLogin : handleRegister}
          >
            {isLogin ? 'Login' : 'Create Account'}
          </Button>

          {/* Switch Between Login and Create Account */}
          <Button
            variant="text"
            color="secondary"
            sx={{ alignSelf: 'flex-end', mt: 1, maxWidth: 400 }}
            onClick={toggleMode}
          >
            {isLogin ? 'Create Account' : 'Already have an account? Login'}
          </Button>
        </Box>
      </div>
    </div>
  );
};

export default LoginSignupPage;
