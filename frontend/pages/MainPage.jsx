import React from 'react';
import Header1 from '../components/Header1'; // Ensure the path to Header1 component is correct
import LeftComponent from '../components/LeftComponent'; // Adjust the path as necessary
import RightComponent from '../components/RightComponent'; // Adjust the path as necessary
import './MainPage.css'; // Import the CSS for MainPage

const MainPage = () => {
  return (
    <div className="main-page">
      <Header1/>
      <div className="content">
        <LeftComponent />
        <RightComponent />
      </div>
    </div>
  );
};

export default MainPage;
