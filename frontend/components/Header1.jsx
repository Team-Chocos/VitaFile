import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Header.css'; // Importing the CSS file
import logo from '../src/assets/logo.png'; //
import searchIcon from '../src/assets/search.png'; 
import messageIcon from '../src/assets/1.png'; 
import alertIcon from '../src/assets/2.png'; 
import exitIcon from '../src/assets/3.png'; 

const Header = ({ toggleSidebar }) => {
  const navigate = useNavigate();

  const handleSearch = () => {
    // Logic to handle search functionality
    console.log("Search initiated");
  };

  const handleExitClick = async () => {
    const token = localStorage.getItem('token');  

    if (token) {
      const response = await fetch('http://localhost:8000/getuser/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const name = await response.text();
        console.log('Name:', name);
      } else {
        console.error('Error:', response.status);
      }
    }

    localStorage.removeItem('token');  
    navigate('/');
  };

  // Function to format the current date
  const formatDate = () => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date().toLocaleDateString('en-US', options);
  };

  const personName = "John Doe"; // Replace with dynamic data if needed

  return (
    <header>
      <div className="search-container">
        <input type="text" placeholder="Search..." className="search-input" />
        <button onClick={handleSearch} className="search-button">
          <img src={searchIcon} alt="Search" className="search-icon" />
        </button>
      </div>
      <div className="person-name-container">
        <span className="person-name">{personName}</span>
      </div>
      <div className="header-right">
        <span className="date-display">{formatDate()}</span>
        <button className="icon-button message-icon">
          <img src={messageIcon} alt="Message" />
        </button>
        <button className="icon-button alert-icon">
          <img src={alertIcon} alt="Alert" />
        </button>
        <button className="icon-button exit-icon" onClick={handleExitClick}>
          <img src={exitIcon} alt="Exit" />
        </button>
      </div>
    </header>
  );
};

export default Header;
