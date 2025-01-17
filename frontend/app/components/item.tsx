"use client";

import React, { useState } from "react";
import { Box, Chip, IconButton } from "@mui/material";
import { Add, Remove } from "@mui/icons-material";
import { blue } from "@mui/material/colors";

export interface ItemProps {
    name: string;
    category: string;
    initialQuantity: number;
}

export const Item: React.FC<ItemProps> = ({
    name,
    category,
    initialQuantity,
}) => {
    const [quantity, setQuantity] = useState(initialQuantity);

    const handleAdd = () => {
        if (quantity > 0) {
            const newQuantity = quantity - 1;
            setQuantity(newQuantity);

            if (newQuantity <= 0) {
                setDisableAdd(true);
            } else {
                setDisableAdd(false);
            }

            if (newQuantity >= initialQuantity) {
                setDisableRemove(true);
            } else {
                setDisableRemove(false);
            }
        }
    };

    const handleRemove = () => {
        if (quantity < initialQuantity) {
            const newQuantity = quantity + 1;
            setQuantity(newQuantity);

            if (newQuantity <= 0) {
                setDisableAdd(true);
            } else {
                setDisableAdd(false);
            }

            if (newQuantity >= initialQuantity) {
                setDisableRemove(true);
            } else {
                setDisableRemove(false);
            }
        }
    };

    const [disableAdd, setDisableAdd] = useState(quantity <= 0);
    const [disableRemove, setDisableRemove] = useState(
        quantity >= initialQuantity
    );

    return (
        <Box
            display="flex"
            padding={"16px 20px"}
            flexDirection="column"
            justifyContent="space-between"
            minWidth={"200px"}
            maxWidth={"300px"}
            gap={"12px"}
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
