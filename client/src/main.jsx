import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { AuthProvider } from './context/AuthContext'
import { GlobalProvider } from './context/GlobalState'
import { ThemeProvider } from './context/ThemeContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <ThemeProvider>
        <GlobalProvider>
          <App />
        </GlobalProvider>
      </ThemeProvider>
    </AuthProvider>
  </React.StrictMode>,
)
