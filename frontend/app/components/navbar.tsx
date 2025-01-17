"use client";

import React, { useState } from "react";
import { AccountCircle, ShoppingCart } from "@mui/icons-material";
import { Box, IconButton, Menu, MenuItem as MuiMenuItem } from "@mui/material";
import { styled } from "@mui/system";
import Image from "next/image";
import { grey, blue } from "@mui/material/colors";

const handleClickProfile = () => {};
const handleLogout = () => {};
const handleCheckout = () => {};

export const NavBar = () => {
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

    const handleMenuClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    return (
        <Box
            display="flex"
            justifyContent="space-between"
            padding="16px 8px"
            borderBottom="1px solid"
            borderColor={grey[200]}
        >
            <Image src="/images/logo.png" alt="logo" width="250" height="80" />
            <Box
                display="flex"
                flexDirection="row"
                justifyContent="flex-end"
                gap="8px"
                alignItems="center"
            >
                <IconButton
                    sx={{
                        padding: 0,
                        borderRadius: "6px",
                        borderStyle: "hidden",
                        "&:hover": {
                            outline: "2px solid",
                            outlineColor: grey[600],
                        },
                    }}
                    onClick={handleCheckout}
                >
                    <ShoppingCart sx={{ color: "black", fontSize: "32px" }} />
                </IconButton>
                <IconButton
                    sx={{
                        padding: 0,
                        borderRadius: "6px",
                        borderStyle: "hidden",
                        "&:hover": {
                            outline: "2px solid",
                            outlineColor: grey[600],
                        },
                    }}
                    onClick={handleMenuClick}
                >
                    <AccountCircle sx={{ fontSize: "32px" }} />
                </IconButton>
                <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleMenuClose}
                >
                    <MenuItem onClick={handleClickProfile}>Profile</MenuItem>
                    <MenuItem onClick={handleLogout}>Log out</MenuItem>
                </Menu>
            </Box>
        </Box>
    );
};

const MenuItem = styled(MuiMenuItem)(
    ({ theme }) => `
  list-style: none;
  padding: 8px;
  border-radius: 8px;
  cursor: default;

  &:last-of-type {
    border-bottom: none;
  }

  &:focus {
    outline: 3px solid ${theme.palette.mode === "dark" ? blue[600] : blue[200]};
    background-color: ${theme.palette.mode === "dark" ? grey[800] : grey[100]};
    color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
  }
`
);
