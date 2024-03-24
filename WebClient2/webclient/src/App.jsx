import logo from './logo.svg';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomeScreen from './Screen/HomeScreen';
import Snap from './Screen/Snap';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route index path="/" element={<HomeScreen />} />
      </Routes>
      <Routes>
        <Route index path="/snap" element={<Snap />} />
      </Routes>
    </Router>
  );
}

export default App;
