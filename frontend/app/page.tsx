"use client";

import { useState } from "react";
import { Item } from "./components/item";
import { NavBar } from "./components/navbar";
import Box from "@mui/material/Box";
import { WelcomeText } from "./components/welcome";

export default function Dashboard() {
    const [quantity, setQuantity] = useState(2);
    return (
        <Box display="flex" flexDirection="column" gap="12px">
            <NavBar />
            <WelcomeText name={"Amy"} />
            <Item
                name="Test"
                maxQuantity={2}
                quantity={quantity}
                setQuantity={setQuantity}
                category="food"
            ></Item>
        </Box>
    );
}
