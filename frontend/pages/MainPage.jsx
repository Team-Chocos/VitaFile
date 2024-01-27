import React, { useState } from 'react';
import Header1 from '../components/Header1';
import LeftComponent from '../components/LeftComponent';
import RightComponent from '../components/RightComponent';
import './MainPage.css';

const MainPage = () => {
  const [chatInput, setChatInput] = useState('');

  const handleTextCopy = (copiedText) => {
    setChatInput(copiedText);
  };

  return (
    <div className="main-page">
      <Header1/>
      <div className="content">
        <LeftComponent onTextCopy={handleTextCopy} />
        <RightComponent chatInput={chatInput} updateChatInput={setChatInput} />
      </div>
    </div>
  );
};

export default MainPage;
