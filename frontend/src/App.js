import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export default function App() {
  const [page, setPage] = useState('pos');

  return (
    <div className="app-container">
      <header className="header">
        <h1>POS PWA</h1>
        <nav className="nav-buttons">
          <button onClick={() => setPage('pos')} className={page === 'pos' ? 'active' : ''}>POS</button>
          <button onClick={() => setPage('negs')} className={page === 'negs' ? 'active' : ''}>Negotiations</button>
        </nav>
      </header>
      <main>
        {page === 'negs' ? <Negotiations /> : <POS />}
      </main>
    </div>
  );
}

function POS() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [pid, setPid] = useState('');

  useEffect(() => { fetchProducts(); }, []);

  async function fetchProducts() {
    try {
      const r = await axios.get(API + '/products/');
      setProducts(r.data);
    } catch (e) {
      console.error(e);
    }
  }

  function addToCartById(id) {
    const p = products.find(x => x.id === Number(id) || x.sku === id);
    if (!p) {
      alert('Product not found');
      return;
    }
    const existingItem = cart.find(item => item.product_id === p.id);
    if (existingItem) {
      update(cart.indexOf(existingItem), 'qty', existingItem.qty + 1);
    } else {
      setCart(c => [...c, { product_id: p.id, name: p.name, qty: 1, list_price: p.list_price, unit_price: p.list_price }]);
    }
  }

  function update(i, field, val) {
    setCart(c => {
      const copy = [...c];
      copy[i][field] = val;
      return copy;
    });
  }

  async function checkout() {
    if (cart.length === 0) {
      alert('Cart is empty');
      return;
    }
    const payload = { cashier: 'clerk1', items: cart.map(c => ({ product_id: c.product_id, qty: c.qty, proposed_unit_price: c.unit_price, proposer: 'customer' })) };
    try {
      const r = await axios.post(API + '/sales/', payload);
      alert('Sale created! ID: ' + r.data.sale_id + ' | Total: ' + r.data.total);
      setCart([]);
    } catch (e) {
      alert('Error creating sale: ' + JSON.stringify(e.response?.data || e));
    }
  }

  const total = cart.reduce((sum, item) => sum + (item.unit_price * item.qty), 0).toFixed(2);

  return (
    <div className="card pos-container">
      <h2>Point of Sale</h2>
      <div className="input-group">
        <input value={pid} onChange={e => setPid(e.target.value)} placeholder='Enter SKU or Product ID' />
        <button onClick={() => { addToCartById(pid); setPid(''); }}>Add to Cart</button>
      </div>
      <div className="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Qty</th>
              <th>List Price</th>
              <th>Unit Price</th>
              <th>Line Total</th>
            </tr>
          </thead>
          <tbody>
            {cart.map((c, i) => (
              <tr key={i}>
                <td>{c.name}</td>
                <td><input type='number' value={c.qty} onChange={e => update(i, 'qty', Number(e.target.value) || 1)} /></td>
                <td>${c.list_price}</td>
                <td><input type='number' value={c.unit_price} onChange={e => update(i, 'unit_price', Number(e.target.value) || c.list_price)} /></td>
                <td>${(c.unit_price * c.qty).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="checkout-section">
        <div className="total-display">Total: ${total}</div>
        <button onClick={checkout} className="checkout-button">Checkout</button>
      </div>
    </div>
  );
}

function Negotiations() {
  const [negs, setNegs] = useState([]);

  async function fetchNegs() {
    try {
      const r = await axios.get(API + '/negotiations/');
      setNegs(r.data);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => { fetchNegs(); }, []);

  async function approve(id) {
    const p = prompt('Enter manager PIN to approve negotiation ID: ' + id);
    if (!p) return;
    try {
      await axios.post(API + `/negotiations/${id}/approve/`, { approver: 'manager', pin: p });
      alert('Negotiation approved!');
      fetchNegs();
    } catch (e) {
      alert('Approval failed: ' + JSON.stringify(e.response?.data || e));
    }
  }

  return (
    <div className="card negotiations-container">
      <h2>Price Negotiations</h2>
      <button onClick={fetchNegs} className="refresh-button">Refresh</button>
      <div className="table-responsive">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Product</th>
              <th>Proposed Price</th>
              <th>Proposer</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {negs.map(n => (
              <tr key={n.id}>
                <td>{n.id}</td>
                <td>{n.product}</td>
                <td>${n.proposed_price}</td>
                <td>{n.proposer}</td>
                <td>{n.status}</td>
                <td>
                  {n.status !== 'approved' && <button onClick={() => approve(n.id)} className="approve-button">Approve</button>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
