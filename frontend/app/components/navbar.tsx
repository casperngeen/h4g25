import { AccountCircle, ShoppingCart } from "@mui/icons-material";
import { Box, IconButton, menuItemClasses } from "@mui/material";
import { Dropdown } from "@mui/base/Dropdown";
import { Menu } from "@mui/base/Menu";
import { MenuItem as BaseMenuItem } from "@mui/base/MenuItem";
import { MenuButton as BaseMenuButton } from "@mui/base/MenuButton";
import { styled } from "@mui/system";
import React from "react";
import { blue, grey } from "@mui/material/colors";
import Image from "next/image";

const handleClickProfile = () => {};

const handleLogout = () => {};

const handleCheckout = () => {};

export const NavBar = () => {
    return (
        <Box
            display="flex"
            justifyContent="space-between"
            padding="16px 8px"
            borderBottom="1px solid"
            borderColor={grey[200]}
        >
            <Image
                src="/images/logo.png"
                alt="logo"
                width="250"
                height="80"
            ></Image>
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
                <Dropdown>
                    <MenuButton
                        sx={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                        }}
                    >
                        <AccountCircle sx={{ fontSize: "32px" }} />
                    </MenuButton>
                    <Menu slots={{ listbox: Listbox }}>
                        <MenuItem onClick={handleClickProfile}>
                            Profile
                        </MenuItem>
                        <MenuItem onClick={handleLogout}>Log out</MenuItem>
                    </Menu>
                </Dropdown>
            </Box>
        </Box>
    );
};

const Listbox = styled("ul")(
    ({ theme }) => `
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.875rem;
    box-sizing: border-box;
    padding: 6px;
    margin: 12px 0;
    min-width: 200px;
    border-radius: 12px;
    overflow: auto;
    outline: 0;
    background: ${theme.palette.mode === "dark" ? grey[900] : "#fff"};
    border: 1px solid ${theme.palette.mode === "dark" ? grey[700] : grey[200]};
    color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
    box-shadow: 0 4px 6px ${
        theme.palette.mode === "dark"
            ? "rgba(0,0,0, 0.50)"
            : "rgba(0,0,0, 0.05)"
    };
    z-index: 1;
    `
);

const MenuItem = styled(BaseMenuItem)(
    ({ theme }) => `
    list-style: none;
    padding: 8px;
    border-radius: 8px;
    cursor: default;
    user-select: none;
  
    &:last-of-type {
      border-bottom: none;
    }
  
    &:focus {
      outline: 3px solid ${
          theme.palette.mode === "dark" ? blue[600] : blue[200]
      };
      background-color: ${
          theme.palette.mode === "dark" ? grey[800] : grey[100]
      };
      color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
    }
  
    &.${menuItemClasses.disabled} {
      color: ${theme.palette.mode === "dark" ? grey[700] : grey[400]};
    }
    `
);

const MenuButton = styled(BaseMenuButton)(
    ({ theme }) => `
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 600;
    line-height: 1.5;
    border-radius: 12px;
    border-style: hidden;
    transition: all 150ms ease;
    cursor: pointer;
    background: white;
    color: ${theme.palette.mode === "dark" ? grey[200] : grey[900]};
    box-shadow: none;
  
    &:hover {
      background: ${theme.palette.mode === "dark" ? grey[800] : grey[50]};
      outline: 2px solid ${grey[600]}
    }
    &:focus-visible {
      outline: none;
      box-shadow: none;
    }
    `
);
