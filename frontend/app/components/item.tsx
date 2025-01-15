"use client";

import React, { useState } from "react";
import { Box, Chip, IconButton } from "@mui/material";
import { Add, Remove } from "@mui/icons-material";
import { blue } from "@mui/material/colors";

interface ItemProps {
    name: string;
    category: string;
    quantity: number;
    maxQuantity: number;
    setQuantity: (value: number) => void;
}

export const Item: React.FC<ItemProps> = ({
    name,
    category,
    maxQuantity,
    quantity,
    setQuantity,
}) => {
    const handleAdd = () => {
        if (quantity > 0) {
            const newQuantity = quantity - 1;
            setQuantity(newQuantity);

            if (newQuantity <= 0) {
                setDisableAdd(true);
            } else {
                setDisableAdd(false);
            }

            if (newQuantity >= maxQuantity) {
                setDisableRemove(true);
            } else {
                setDisableRemove(false);
            }
        }
    };

    const handleRemove = () => {
        if (quantity < maxQuantity) {
            const newQuantity = quantity + 1;
            setQuantity(newQuantity);

            if (newQuantity <= 0) {
                setDisableAdd(true);
            } else {
                setDisableAdd(false);
            }

            if (newQuantity >= maxQuantity) {
                setDisableRemove(true);
            } else {
                setDisableRemove(false);
            }
        }
    };

    const [disableAdd, setDisableAdd] = useState(quantity <= 0);
    const [disableRemove, setDisableRemove] = useState(quantity >= maxQuantity);

    return (
        <Box
            display="flex"
            padding={"8px"}
            flexDirection="column"
            justifyContent="space-between"
            maxWidth={"200px"}
            gap={"8px"}
            sx={{
                backgroundColor: blue[50],
                borderStyle: "hidden",
                borderRadius: "8px",
            }}
        >
            <div style={{ textAlign: "center", fontSize: "20px" }}>{name}</div>
            <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
            >
                <Chip
                    label={category}
                    sx={{
                        fontSize: "16px",
                        backgroundColor: blue[100],
                    }}
                ></Chip>
                <div style={{ fontSize: "16px" }}>Qty: {quantity}</div>
            </Box>
            <Box display="flex" justifyContent="flex-end" gap="4px">
                <IconButton onClick={handleAdd} disabled={disableAdd}>
                    <Add sx={{ fontSize: "24px" }} />
                </IconButton>
                <IconButton onClick={handleRemove} disabled={disableRemove}>
                    <Remove sx={{ fontSize: "24px" }} />
                </IconButton>
            </Box>
        </Box>
    );
};
