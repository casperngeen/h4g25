import { AccountCircle, ShoppingCart } from "@mui/icons-material";
import { Box } from "@mui/material";
import React from "react";

export const NavBar = () => {
    return (
        <Box>
            <ShoppingCart></ShoppingCart>
            <AccountCircle></AccountCircle>
        </Box>
    );
};
