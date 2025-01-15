"use client";

import { useEffect, useState } from "react";
import { Item, ItemProps } from "./components/item";
import { NavBar } from "./components/navbar";
import Box from "@mui/material/Box";
import { WelcomeText } from "./components/welcome";
import Container from "@mui/material/Container";

const mockItems: ItemProps[] = [
    { name: "Desk Chair", category: "food", initialQuantity: 10 },
    { name: "Novel", category: "electronics", initialQuantity: 1 },
    { name: "Headphones", category: "clothing", initialQuantity: 9 },
    { name: "Tablet", category: "electronics", initialQuantity: 1 },
    { name: "Tablet", category: "food", initialQuantity: 10 },
    { name: "Headphones", category: "toys", initialQuantity: 2 },
    { name: "Tablet", category: "furniture", initialQuantity: 10 },
    { name: "Apple", category: "furniture", initialQuantity: 4 },
    { name: "Laptop", category: "clothing", initialQuantity: 6 },
    { name: "T-Shirt", category: "furniture", initialQuantity: 6 },
];

export default function Dashboard() {
    const [items, setItems] = useState<ItemProps[]>(mockItems);
    const API_URL = "http://localhost:3001";

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${API_URL}/items`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const result = await response.json();
                setItems(result);
            } catch (err) {
                console.error("Failed to fetch items:", err);
            }
        };

        fetchData();
    }, []);

    return (
        <Container
            sx={{
                padding: "24px",
                overflowY: "auto",
            }}
        >
            <Box display="flex" flexDirection="column" gap="12px">
                <NavBar />
                <WelcomeText name={"Amy"} />
                <Box
                    sx={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: 3,
                        paddingTop: "16px",
                        justifyContent: "flex-start",
                        overflowY: "auto",
                        padding: "16px",
                    }}
                >
                    {items.map((item, index) => (
                        <Box key={index}>
                            <Item
                                name={item.name}
                                initialQuantity={item.initialQuantity}
                                category={item.category}
                            />
                        </Box>
                    ))}
                </Box>
            </Box>
        </Container>
    );
}
