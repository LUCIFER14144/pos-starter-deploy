import React, { useEffect, useState } from 'react';
import axios from 'axios';
const API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
export default function App(){
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [pid, setPid] = useState('');
  const [page, setPage] = useState('pos');
  useEffect(()=>{ fetchProducts(); },[]);
  async function fetchProducts(){
    try{ const r = await axios.get(API+'/products/'); setProducts(r.data); }catch(e){console.error(e);} }
  function addToCartById(id){
    const p = products.find(x=>x.id===Number(id)||x.sku===id);
    if(!p){ alert('Product not found'); return; }
    setCart(c=>[...c,{ product_id: p.id, name: p.name, qty:1, list_price: p.list_price, unit_price: p.list_price }]);
  }
  function update(i, field, val){ setCart(c=>{ const copy=[...c]; copy[i][field]=val; return copy; }); }
  async function checkout(){
    if(cart.length===0){ alert('empty'); return; }
    const payload = { cashier: 'clerk1', items: cart.map(c=>({ product_id: c.product_id, qty: c.qty, proposed_unit_price: c.unit_price, proposer: 'customer' })) };
    try{ const r = await axios.post(API+'/sales/', payload); alert('Sale created id:'+r.data.sale_id+' total:'+r.data.total); setCart([]); }catch(e){ alert('error '+JSON.stringify(e.response?.data||e)); }
  }
  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <div style={{marginBottom:10}}><button onClick={()=>setPage('pos')}>POS</button> <button onClick={()=>setPage('negs')}>Negotiations</button></div>
      {page==='negs' ? <Negotiations/> : (
      <div style={{padding:20,fontFamily:'Arial'}}>
      <h2>POS PWA (minimal)</h2>
      <div>
        <input value={pid} onChange={e=>setPid(e.target.value)} placeholder='SKU or ID' />
        <button onClick={()=>{addToCartById(pid); setPid('');}}>Add</button>
      </div>
      <table style={{width:'100%',marginTop:10,borderCollapse:'collapse'}}>
        <thead><tr><th>Product</th><th>Qty</th><th>List</th><th>Unit</th><th>Line</th></tr></thead>
        <tbody>
          {cart.map((c,i)=> (
            <tr key={i}>
              <td>{c.name}</td>
              <td><input type='number' value={c.qty} onChange={e=>update(i,'qty',Number(e.target.value)||1)} /></td>
              <td>{c.list_price}</td>
              <td><input type='number' value={c.unit_price} onChange={e=>update(i,'unit_price',Number(e.target.value)||c.list_price)} /></td>
              <td>{(c.unit_price*c.qty).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{marginTop:10}}>
        <button onClick={checkout}>Checkout</button>
      </div>
      </div>
      )}
    </div>
  );
}

function Negotiations(){
  const [negs, setNegs] = React.useState([]);
  async function fetchNegs(){ try{ const r = await axios.get(API+'/negotiations/'); setNegs(r.data); }catch(e){console.error(e);} }
  React.useEffect(()=>{ fetchNegs(); },[]);
  async function approve(id){
    const p = prompt('Enter manager PIN to approve negotiation id:'+id);
    if(!p) return;
    try{
      const r = await axios.post(API+`/negotiations/${id}/approve/`, { approver:'manager', pin: p });
      alert('approved');
      fetchNegs();
    }catch(e){ alert('approval failed: '+JSON.stringify(e.response?.data||e)); }
  }
  return (
    <div style={{padding:20}}>
      <h3>Negotiations</h3>
      <button onClick={fetchNegs}>Refresh</button>
      <table style={{width:'100%',marginTop:10,borderCollapse:'collapse'}}>
        <thead><tr><th>ID</th><th>Product</th><th>Proposed</th><th>Proposer</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          {negs.map(n=> (
            <tr key={n.id}><td>{n.id}</td><td>{n.product}</td><td>{n.proposed_price}</td><td>{n.proposer}</td><td>{n.status}</td><td>{n.status!=='approved' && <button onClick={()=>approve(n.id)}>Approve</button>}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
