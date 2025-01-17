"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";

const AdminDashboard = () => {
    const [voucherRequests, setVoucherRequests] = useState<any[]>([]);
    const [productRequests, setProductRequests] = useState<any[]>([]);
    const [inventory, setInventory] = useState<any[]>([]);
    const [auditLogs, setAuditLogs] = useState<any[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const voucherResponse = await fetch("/api/voucher-requests");
                const productResponse = await fetch("/api/product-requests");
                const inventoryResponse = await fetch("/api/inventory");

                const voucherData = await voucherResponse.json();
                const productData = await productResponse.json();
                const inventoryData = await inventoryResponse.json();

                setVoucherRequests(voucherData);
                setProductRequests(productData);
                setInventory(inventoryData);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    const approveVoucher = async (voucherId: string) => {
        try {
            const response = await fetch(
                `/api/voucher-requests/${voucherId}/approve`,
                { method: "POST" }
            );
            const updatedVoucher = await response.json();

            setVoucherRequests(
                voucherRequests.map((voucher) =>
                    voucher.id === voucherId ? updatedVoucher : voucher
                )
            );
            setAuditLogs([...auditLogs, `Voucher ${voucherId} approved.`]);
        } catch (error) {
            console.error("Error approving voucher:", error);
        }
    };

    const rejectVoucher = async (voucherId: string) => {
        try {
            const response = await fetch(
                `/api/voucher-requests/${voucherId}/reject`,
                { method: "POST" }
            );
            const updatedVoucher = await response.json();

            setVoucherRequests(
                voucherRequests.map((voucher) =>
                    voucher.id === voucherId ? updatedVoucher : voucher
                )
            );
            setAuditLogs([...auditLogs, `Voucher ${voucherId} rejected.`]);
        } catch (error) {
            console.error("Error rejecting voucher:", error);
        }
    };

    const approveProduct = async (productId: string) => {
        try {
            const response = await fetch(
                `/api/product-requests/${productId}/approve`,
                { method: "POST" }
            );
            const updatedProduct = await response.json();

            setProductRequests(
                productRequests.map((product) =>
                    product.id === productId ? updatedProduct : product
                )
            );
            setAuditLogs([...auditLogs, `Product ${productId} approved.`]);
        } catch (error) {
            console.error("Error approving product:", error);
        }
    };

    const rejectProduct = async (productId: string) => {
        try {
            const response = await fetch(
                `/api/product-requests/${productId}/reject`,
                { method: "POST" }
            );
            const updatedProduct = await response.json();

            setProductRequests(
                productRequests.map((product) =>
                    product.id === productId ? updatedProduct : product
                )
            );
            setAuditLogs([...auditLogs, `Product ${productId} rejected.`]);
        } catch (error) {
            console.error("Error rejecting product:", error);
        }
    };

    const updateInventory = async (productId: string, quantity: number) => {
        try {
            const response = await fetch(`/api/inventory/${productId}/update`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ quantity }),
            });
            const updatedInventory = await response.json();

            setInventory(
                inventory.map((item) =>
                    item.productId === productId ? updatedInventory : item
                )
            );
            setAuditLogs([
                ...auditLogs,
                `Inventory updated for product ${productId}.`,
            ]);
        } catch (error) {
            console.error("Error updating inventory:", error);
        }
    };

    return (
        <div className="admin-dashboard">
            <div className="sidebar">
                {/* Position logo at top right */}
                <Image
                    src="/images/logo.png"
                    alt="Welfare Centre Logo"
                    width={150}
                    height={150}
                    className="logo"
                />
            </div>
            <div className="content">
                <div className="dashboard-header">
                    <h1>Admin Dashboard</h1>
                    <button className="generate-report-btn">
                        Generate Report
                    </button>
                </div>

                <div className="task-section">
                    <h2>Voucher Requests</h2>
                    <table className="task-table">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {voucherRequests.map((voucher) => (
                                <tr key={voucher.id}>
                                    <td>{voucher.user}</td>
                                    <td>{voucher.status}</td>
                                    <td>
                                        <button
                                            className="approve-btn"
                                            onClick={() =>
                                                approveVoucher(voucher.id)
                                            }
                                        >
                                            Approve
                                        </button>
                                        <button
                                            className="reject-btn"
                                            onClick={() =>
                                                rejectVoucher(voucher.id)
                                            }
                                        >
                                            Reject
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="inventory-section">
                    <h2>Product Requests</h2>
                    <table className="inventory-table">
                        <thead>
                            <tr>
                                <th>Product Name</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {productRequests.map((product) => (
                                <tr key={product.id}>
                                    <td>{product.name}</td>
                                    <td>
                                        <button
                                            className="approve-btn"
                                            onClick={() =>
                                                approveProduct(product.id)
                                            }
                                        >
                                            Approve
                                        </button>
                                        <button
                                            className="reject-btn"
                                            onClick={() =>
                                                rejectProduct(product.id)
                                            }
                                        >
                                            Reject
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="audit-section">
                    <h2>Audit Logs</h2>
                    <ul className="audit-log-list">
                        {auditLogs.map((log, index) => (
                            <li className="audit-log-item" key={index}>
                                <span>{log}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
