import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import logo from '../src/assets/Logo1.png';
import logo1 from '../src/assets/google.png';
import logo2 from '../src/assets/Logo2.png';

const Login = () => {
    const navigate = useNavigate();

    const handleLogin = (event) => {
        event.preventDefault();
        navigate('/family');
    };

    const handleLoginNavigation = () => {
        navigate('/signup');
    };

    return (
        <div className="login-page">
            <div className="left-container">
                <div className="login-container">
                    <div className="login-card">
                        <div className="logo-container">
                            <img src={logo} className="logo" alt="Logo" />
                            <span className="logo-text"><h1>VitaFile</h1></span>
                        </div>
                        <h2>Login to your account</h2>
                        <br />
                        <form className="login-form" onSubmit={handleLogin}>
                            <div className="input-group">
                                <input type="text" id="username" name="username" placeholder="Username" required />
                            </div>
                            <div className="input-group">
                                <input type="password" id="password" name="password" placeholder="Password" required />
                            </div>
                            <div className="footer-group">
                                <button type="submit" className="login-button">Login</button>
                                <div className="media-options">
                                    <button type="button" className="login-button1">
                                        <img src={logo1} className="logo1" alt="Google logo" />
                                        Login with Google
                                    </button>
                                </div>
                                <p>Already have an account? <span onClick={handleLoginNavigation} className="signup-link">Signup</span></p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div className="right-container">
                {/* Right container content (if any) */}
            </div>
        </div>
    );
};

export default Login;
