"use client";

import { useState } from "react";
import { Item } from "./components/item";

export default function Dashboard() {
    const [quantity, setQuantity] = useState(2);
    return (
        <Item
            name="Test"
            maxQuantity={2}
            quantity={quantity}
            setQuantity={setQuantity}
            category="food"
        ></Item>
    );
}
