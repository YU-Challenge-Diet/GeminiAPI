import React, { useState } from 'react';
import './../css/Index.css';
import './../css/Switch.css';
import { useNavigate } from 'react-router-dom';
const HomeScreen = () => {
  const [toggle, setToggle] = useState(false);
  const navigate = useNavigate();

  const toComponentSnap = () => {
    navigate('/Snap', { state: { mode: toggle } });
  };
  const handleChange = () => {
    setToggle(!toggle);
  };

  return (
    <div className="screen">
      <div className="outerScreen">
        <div className="text-row">
          <h1 className="header">
            Capture <br /> your <br /> health.
          </h1>
        </div>
        <div className="text-row">
          <div className="switch-wrapper">
            {!toggle ? (
              <>
                <div className="center-align">
                  <button className="btn" disabled>
                    Cook at Home
                  </button>
                </div>
              </>
            ) : (
              <p>Cook at Home</p>
            )}

            <label className="switch">
              <input type="checkbox" checked={toggle} onChange={handleChange} />
              <span className="slider round"></span>
            </label>
            {toggle ? (
              <>
                <div className="center-align">
                  <button className="btn" disabled>
                    Eat a meal
                  </button>
                </div>
              </>
            ) : (
              <p>Eat a meal</p>
            )}
          </div>
        </div>
        <div className="text-row">
          <div className="button-wrapper">
            <button
              onClick={() => {
                toComponentSnap();
              }}
            >
              Snap your food!
            </button>
          </div>
        </div>
        <div className="text-row">
          Start your tasty path to wellness with <br /> <b>Eat healthy.</b>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
