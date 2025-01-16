'use client';

import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [voucherRequests, setVoucherRequests] = useState<any[]>([]);
  const [productRequests, setProductRequests] = useState<any[]>([]);
  const [inventory, setInventory] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  useEffect(() => {
    setVoucherRequests([
      { id: 'v1', name: 'Voucher A', status: 'Pending' },
      { id: 'v2', name: 'Voucher B', status: 'Pending' },
    ]);
    setProductRequests([
      { id: 'p1', name: 'Product A', status: 'Pending' },
      { id: 'p2', name: 'Product B', status: 'Pending' },
    ]);
    setInventory([
      { productId: 'p1', productName: 'Product A', quantity: 10 },
      { productId: 'p2', productName: 'Product B', quantity: 15 },
    ]);
  }, []);

  const approveVoucher = (voucherId: string) => {
    setVoucherRequests(voucherRequests.map((voucher) =>
      voucher.id === voucherId ? { ...voucher, status: 'Approved' } : voucher
    ));
    setAuditLogs([...auditLogs, `Voucher ${voucherId} approved.`]);
  };

  const rejectVoucher = (voucherId: string) => {
    setVoucherRequests(voucherRequests.map((voucher) =>
      voucher.id === voucherId ? { ...voucher, status: 'Rejected' } : voucher
    ));
    setAuditLogs([...auditLogs, `Voucher ${voucherId} rejected.`]);
  };

  const approveProduct = (productId: string) => {
    setProductRequests(productRequests.map((product) =>
      product.id === productId ? { ...product, status: 'Approved' } : product
    ));
    setAuditLogs([...auditLogs, `Product ${productId} approved.`]);
  };

  const rejectProduct = (productId: string) => {
    setProductRequests(productRequests.map((product) =>
      product.id === productId ? { ...product, status: 'Rejected' } : product
    ));
    setAuditLogs([...auditLogs, `Product ${productId} rejected.`]);
  };

  const updateInventory = (productId: string, quantity: number) => {
    setInventory(inventory.map((item) =>
      item.productId === productId ? { ...item, quantity } : item
    ));
    setAuditLogs([...auditLogs, `Inventory updated for product ${productId}.`]);
  };

  const generateReport = () => {
    setReports([
      {
        type: 'Weekly Requests',
        data: voucherRequests.length + productRequests.length,
      },
      {
        type: 'Inventory Summary',
        data: inventory.reduce((total, item) => total + item.quantity, 0),
      },
    ]);
  };

  return (
    <div className="admin-dashboard">
      <header className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <button onClick={generateReport} className="generate-report-btn">Generate Reports</button>
      </header>

      <section className="task-section">
        <h2>Voucher Requests</h2>
        <ul className="task-list">
          {voucherRequests.map((voucher) => (
            <li key={voucher.id} className="task-item">
              <span>{voucher.name}</span>
              <button onClick={() => approveVoucher(voucher.id)} className="approve-btn">Approve</button>
              <button onClick={() => rejectVoucher(voucher.id)} className="reject-btn">Reject</button>
            </li>
          ))}
        </ul>
      </section>

      <section className="task-section">
        <h2>Product Requests</h2>
        <ul className="task-list">
          {productRequests.map((product) => (
            <li key={product.id} className="task-item">
              <span>{product.name}</span>
              <button onClick={() => approveProduct(product.id)} className="approve-btn">Approve</button>
              <button onClick={() => rejectProduct(product.id)} className="reject-btn">Reject</button>
            </li>
          ))}
        </ul>
      </section>

      <section className="inventory-section">
        <h2>Inventory Management</h2>
        <ul className="inventory-list">
          {inventory.map((item) => (
            <li key={item.productId} className="inventory-item">
              <span>{item.productName} - {item.quantity}</span>
              <input
                type="number"
                value={item.quantity}
                onChange={(e) => updateInventory(item.productId, Number(e.target.value))}
                className="inventory-update-input"
              />
            </li>
          ))}
        </ul>
      </section>

      <section className="audit-section">
        <h2>Audit Logs</h2>
        <ul className="audit-log-list">
          {auditLogs.map((log, index) => (
            <li key={index} className="audit-log-item">{log}</li>
          ))}
        </ul>
      </section>

      <section className="report-section">
        <h2>Reports</h2>
        <ul className="report-list">
          {reports.map((report, index) => (
            <li key={index} className="report-item">
              <h3>{report.type}</h3>
              <p>{report.data}</p>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default AdminDashboard;
