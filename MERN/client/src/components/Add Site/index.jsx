import React, { useState, useEffect } from 'react';
import './Styl.css';

function Sites() {
  const initialData = JSON.parse(localStorage.getItem('siteData')) || [];
  const [data, setData] = useState(initialData);
  const [editIdx, setEditIdx] = useState(-1);
  const [input, setInput] = useState({
    companyName: '',
    siteName: '',
    link: '',
  });

  const handleChange = e => {
    setInput({
      ...input,
      [e.target.name]: e.target.value,
    });
  };

  const handleAdd = () => {
    setData([...data, input]);
    setInput({ companyName: '', siteName: '', link: '' });
  };

  const handleDelete = idx => {
    setData(data.filter((d, i) => i !== idx));
  };

  const handleEdit = idx => {
    setEditIdx(idx);
    setInput(data[idx]);
  };

  const handleUpdate = () => {
    const updatedData = [...data];
    updatedData[editIdx] = input;
    setData(updatedData);
    setEditIdx(-1);
    setInput({ companyName: '', siteName: '', link: '' });
  };

  useEffect(() => {
    localStorage.setItem('siteData', JSON.stringify(data));
  }, [data]);

  return (
    <div style={{position:"relative",top:"85px"}}>
  <input name="companyName" onChange={handleChange} value={input.companyName} placeholder="Company Name"  />
  <input name="siteName" onChange={handleChange} value={input.siteName} placeholder="Site Name" />
  <input name="link" onChange={handleChange} value={input.link} placeholder="Link" />
  <button className={editIdx >= 0 ? "edit" : "add"} onClick={editIdx >= 0 ? handleUpdate : handleAdd}>{editIdx >= 0 ? 'Update' : 'Add'}</button>
  <table>
    <thead>
      <tr>
        <th>Company Name</th>
        <th>Site Name</th>
        <th>Link</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {data.map((d, idx) => (
        <tr key={idx}>
          <td>{d.companyName}</td>
          <td>{d.siteName}</td>
          <td>{d.link}</td>
          <td>
            <button className="delete" onClick={() => handleDelete(idx)}>Delete</button>
            <button className="edit" onClick={() => handleEdit(idx)}>Edit</button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

  )
}

export default Sites;
