import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mail, Lock, User, ArrowRight } from 'lucide-react'; 
import Image from 'next/image';
import { Container, Typography, Button, TextField, Select, MenuItem, InputLabel, FormControl, Box, IconButton, InputAdornment } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';

const API_BASE_URL = 'https://127.0.0.1:5000'; 

const LoginSignupPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [userType, setUserType] = useState(''); // Resident or Admin
  const [error, setError] = useState('');

  const toggleMode = () => setIsLogin(!isLogin);

  const handleTogglePassword = () => {
    setPasswordVisible(!passwordVisible);
  };

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Please enter both email and password.');
      return;
    }

    const loginData = {
      email,
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
        console.log(result);
      } else {
        setError(result.Error || 'Login failed');
      }
    } catch (error) {
      console.error('Login failed', error);
      setError('An error occurred while logging in.');
    }
  };

  const handleRegister = async () => {
    if (!name || !email || !password || !userType) {
      setError('Please fill in all fields.');
      return;
    }

    const registerData = {
      name,
      email,
      password,
      userType, // resident or admin
    };

    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registerData),
      });

      const result = await response.json();
      if (response.ok) {
        console.log(result);
      } else {
        setError(result.Error || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration failed', error);
      setError('An error occurred while registering.');
    }
  };

  return (
    <div className="flex flex-col md:flex-row h-screen bg-gray-100">
      {/* Right side panel */}
      <div className="w-full md:w-1/2 bg-gray-100 p-8 md:p-16 flex flex-col justify-center items-center">
        {/* Header with Logo and Welcome Message */}
        <Box display="flex" flexDirection="column" alignItems="center" textAlign="center">
          <Image
            src="/images/mwh_logo.png"
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
          {!isLogin && (
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
          )}

          {/* Username Field */}
          <TextField
            fullWidth
            label="Enter Name"
            variant="outlined"
            margin="normal"
            sx={{ maxWidth: 400 }}
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isLogin} 
          />

          {/* Email Field */}
          {!isLogin && (
            <TextField
              fullWidth
              label="Enter Email"
              variant="outlined"
              margin="normal"
              sx={{ maxWidth: 400 }}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          )}

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
